#!/usr/bin/env python3
"""Embed a Singlepane Docs add-in variable store (sp_docs_store) into a
generated .pptx or .docx, replicating the exact format the add-in itself
persists (verified against a real PowerPoint add-in save; Word uses the same
mechanism via the donor's own part layout).

Usage:
  python3 graft_sp_store.py <target.pptx|docx> <donor.pptx|docx> <store.json> [-o out]
  python3 graft_sp_store.py --validate-only <store.json>

- target: a freshly generated file containing <<tags>> and NO webextension parts
  (plain python-pptx / python-docx output qualifies).
- donor:  any file of the SAME type previously saved with the Singlepane add-in
  loaded — it supplies the add-in reference and task-pane wiring. A donor saved
  by a dev sideload carries a dev reference; use a donor from the same add-in
  installation the recipient uses.
- store.json: the sp_docs_store object (see references/variables-and-store.md).
  Validated before grafting; validation errors abort.

Writes the result to -o/--output (default: overwrite target in place).
Stdlib only — no dependencies.
"""

import argparse
import json
import re
import sys
import uuid
import zipfile
from xml.sax.saxutils import escape

TASKPANES_REL_TYPE = "http://schemas.microsoft.com/office/2011/relationships/webextensiontaskpanes"
CT_TASKPANES = "application/vnd.ms-office.webextensiontaskpanes+xml"
CT_WEBEXTENSION = "application/vnd.ms-office.webextension+xml"
STORE_KEY = "sp_docs_store"

MONTH_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_AGG_RE = re.compile(
    r"^(Total Year|Q[1-4]|(%s)(YTD|TTM|BOY)|(%s))$" % ("|".join(MONTH_SHORT), "|".join(MONTH_SHORT))
)
KNOWN_VERSIONS = (
    {"Actual", "Proforma", "LY_Actual", "Var_Budget", "Var_LY_Actual", "Budget"}
    | {f"Budget{i}" for i in range(1, 13)}
    | {f"Forecast{i}" for i in range(1, 13)}
)
GLOBAL_VALUE_TYPES = {"month", "year", "number", "text", "date"}
KNOWN_MODIFIERS = {
    "currency", "percent", "number", "abbrev", "abs", "updown", "words",
    "date", "monthlong", "monthshort", "upper", "lower", "capitalize", "sign", "paren",
}
REF_RE = re.compile(r"\{([^{}]+)\}")

QUERY_FIELDS = {
    "financials": ["codes", "usali", "month", "year", "version"],
    "str": ["code", "date", "aggregateType", "metric", "subjectCompMarket", "segment"],
    "otb": ["code", "dailyOrMonthly", "stayDate", "targetSet", "periodType", "metric", "segment", "asOfDate"],
    "interest_rate": ["benchmarkRate", "date", "asOfDate"],
}


def norm(name):
    return re.sub(r"\s+", " ", name.strip()).lower()


def field_refs(value):
    return [norm(m.group(1)) for m in REF_RE.finditer(value)]


def validate_store(store):
    """Return (errors, warnings). Errors abort the graft."""
    errors, warnings = [], []
    if not isinstance(store, dict):
        return ["store.json must contain a JSON object"], []
    if store.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if store.get("viewMode") not in ("tags", "values"):
        errors.append('viewMode must be "tags" or "values" (generate with "tags")')
    variables = store.get("variables")
    if not isinstance(variables, list) or not variables:
        return errors + ["variables must be a non-empty array"], warnings

    names = {}
    for i, v in enumerate(variables):
        label = f"variables[{i}]" + (f' ("{v.get("name")}")' if isinstance(v, dict) and v.get("name") else "")
        if not isinstance(v, dict):
            errors.append(f"{label}: not an object")
            continue
        name = v.get("name")
        if not name or not isinstance(name, str) or not name.strip():
            errors.append(f"{label}: missing name")
            continue
        key = norm(name)
        if key in names:
            errors.append(f'{label}: duplicate name (case-insensitive) with "{names[key]}"')
        names[key] = name
        vid = v.get("id")
        if not vid or not isinstance(vid, str):
            errors.append(f"{label}: missing id (use a uuid4)")
        else:
            try:
                uuid.UUID(vid)
            except ValueError:
                errors.append(f"{label}: id is not a valid UUID")
        for mod in v.get("defaultModifiers") or []:
            if not isinstance(mod, dict) or "name" not in mod:
                errors.append(f"{label}: defaultModifiers entries need a name")
            elif mod["name"] not in KNOWN_MODIFIERS:
                errors.append(f'{label}: unknown modifier "{mod["name"]}"')
            if isinstance(mod, dict) and not isinstance(mod.get("args", []), list):
                errors.append(f"{label}: modifier args must be an array")

    globals_by_key = {
        norm(v["name"]): v for v in variables
        if isinstance(v, dict) and v.get("kind") == "global" and isinstance(v.get("name"), str)
    }

    for i, v in enumerate(variables):
        if not isinstance(v, dict) or not isinstance(v.get("name"), str):
            continue
        label = f'"{v["name"]}"'
        kind = v.get("kind")
        if kind == "global":
            vt = v.get("valueType")
            if vt not in GLOBAL_VALUE_TYPES:
                errors.append(f"{label}: valueType must be one of {sorted(GLOBAL_VALUE_TYPES)}")
            value = v.get("value")
            if value is None or (isinstance(value, str) and value.strip() == ""):
                errors.append(f"{label}: global needs a value")
            elif vt == "month" and str(value) not in MONTH_SHORT:
                warnings.append(f'{label}: month value "{value}" is not canonical 3-letter ("Jun")')
            elif vt == "year" and not (isinstance(value, int) and 1900 <= value <= 2200):
                warnings.append(f'{label}: year value "{value}" is not a plausible 4-digit number')
            elif vt == "date" and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(value)):
                warnings.append(f'{label}: date value "{value}" is not YYYY-MM-DD')
        elif kind == "query":
            q = v.get("query")
            if not isinstance(q, dict) or q.get("type") not in QUERY_FIELDS:
                errors.append(f"{label}: query.type must be one of {sorted(QUERY_FIELDS)}")
                continue
            qtype = q["type"]
            fields = []
            for f in QUERY_FIELDS[qtype]:
                if f not in q:
                    errors.append(f"{label}: query missing field {f}")
                elif f == "codes":
                    if not isinstance(q[f], list) or not q[f]:
                        errors.append(f"{label}: codes must be a non-empty array of strings")
                    else:
                        fields += [(f, c) for c in q[f]]
                elif not isinstance(q[f], str):
                    errors.append(f"{label}: query field {f} must be a string")
                else:
                    fields.append((f, q[f]))
            # {Global} references must resolve to a global variable
            for f, value in fields:
                for ref in field_refs(value):
                    if ref not in globals_by_key:
                        target = names.get(ref)
                        if target:
                            errors.append(
                                f'{label}: field {f} references {{{target}}} which is not a global '
                                f"(query fields may only reference globals)"
                            )
                        else:
                            errors.append(f'{label}: field {f} references unknown global "{{{ref}}}"')
            # vocabulary spot-checks on literal (non-interpolated) fields
            def literal(f):
                s = q.get(f)
                return s if isinstance(s, str) and not REF_RE.search(s) else None
            if qtype == "financials":
                m = literal("month")
                if m and not MONTH_AGG_RE.match(m):
                    warnings.append(f'{label}: month "{m}" is not a known month/aggregate')
                ver = literal("version")
                if ver and ver not in KNOWN_VERSIONS:
                    warnings.append(f'{label}: version "{ver}" is not a standard version (ok if company-specific)')
                y = literal("year")
                if y and not re.match(r"^\d{4}$", y):
                    warnings.append(f'{label}: year "{y}" is not a 4-digit year')
                u = q.get("usali")
                if isinstance(u, str) and REF_RE.search(u) is None and " - " not in u and not u.isupper():
                    warnings.append(f'{label}: usali "{u}" has no " - NNN" department suffix — verify the exact string')
            if qtype == "str":
                agg = literal("aggregateType")
                if agg and agg not in {"day", "month", "monthToDate", "currentWeek",
                                       "running28Days", "yearToDate", "running3Month", "running12Month"}:
                    errors.append(f'{label}: aggregateType "{agg}" invalid (case-sensitive)')
            if qtype == "otb":
                dm = literal("dailyOrMonthly")
                if dm and dm not in {"daily", "monthly"}:
                    errors.append(f'{label}: dailyOrMonthly "{dm}" must be daily|monthly')
                pt = literal("periodType")
                if pt and pt not in {"ty", "ly"}:
                    errors.append(f'{label}: periodType "{pt}" must be ty|ly')
            if qtype == "interest_rate":
                b = literal("benchmarkRate")
                if b and b.upper() not in {"SOFR", "SONIA", "T10YR"}:
                    errors.append(f'{label}: benchmarkRate "{b}" must be SOFR|SONIA|T10YR')
        elif kind == "computed":
            expr = v.get("expression")
            if not expr or not isinstance(expr, str) or not expr.strip():
                errors.append(f"{label}: computed variable needs an expression")
            else:
                for ref in re.findall(r"\[([^\[\]]+)\]", expr):
                    if norm(ref) not in names:
                        errors.append(f'{label}: expression references undefined variable "[{ref}]"')
                if expr.count("(") != expr.count(")") or expr.count("[") != expr.count("]"):
                    errors.append(f"{label}: unbalanced brackets/parens in expression")
        else:
            errors.append(f'{label}: kind must be global|query|computed, got "{kind}"')

    return errors, warnings


def find_webextension_paths(names, prefix):
    """Donor part paths under <prefix>/webextensions/."""
    base = f"{prefix}/webextensions/"
    return [n for n in names if n.startswith(base)]


def graft(target_path, donor_path, store, out_path):
    dz = zipfile.ZipFile(donor_path)
    donor_names = dz.namelist()

    prefix = None
    for p in ("ppt", "word"):
        if any(n.startswith(f"{p}/webextensions/") for n in donor_names):
            prefix = p
            break
    if prefix is None:
        sys.exit(
            "error: donor has no webextensions part. The donor must be a file that was "
            "saved in PowerPoint/Word WITH the Singlepane add-in loaded (open it, open the "
            "Singlepane pane, make any change, save)."
        )

    we_paths = find_webextension_paths(donor_names, prefix)
    webext_parts = [n for n in we_paths if re.search(r"/webextension\d+\.xml$", n)]
    store_part = None
    for n in webext_parts:
        if STORE_KEY in dz.read(n).decode("utf-8", "replace"):
            store_part = n
            break
    if store_part is None:
        if len(webext_parts) == 1:
            store_part = webext_parts[0]  # add-in loaded but never saved variables
        else:
            sys.exit(
                f"error: could not identify the Singlepane webextension part in the donor "
                f"(found {len(webext_parts)} webextension parts, none containing {STORE_KEY}). "
                f"Save the donor once with at least one variable defined in the pane."
            )

    # Replace the donor's <we:properties> block with our store + auto-show pane.
    donor_we = dz.read(store_part).decode("utf-8")
    if "<we:properties" not in donor_we:
        sys.exit(f"error: donor part {store_part} has no <we:properties> element")
    prop_value = escape(json.dumps(json.dumps(store)), {'"': "&quot;"})
    head = donor_we[: donor_we.index("<we:properties")]
    tail = donor_we[donor_we.index("</we:properties>") + len("</we:properties>"):]
    new_we = (
        head
        + f'<we:properties><we:property name="{STORE_KEY}" value="{prop_value}"/>'
        + '<we:property name="Office.AutoShowTaskpaneWithDocument" value="true"/>'
        + "</we:properties>"
        + tail
    )

    with zipfile.ZipFile(target_path) as zin:
        order = zin.namelist()
        items = {n: zin.read(n) for n in order}

    if any(n.startswith(f"{prefix}/webextensions/") for n in order):
        sys.exit("error: target already contains webextension parts — graft into a clean generated file")
    if not any(n.startswith(f"{prefix}/") for n in order):
        sys.exit(f"error: target does not look like a {prefix} package (donor is {prefix}); host types must match")

    # Copy every webextensions part from the donor, substituting our store part.
    for n in we_paths:
        items[n] = new_we.encode("utf-8") if n == store_part else dz.read(n)

    # Content-type overrides.
    ct = items["[Content_Types].xml"].decode("utf-8")
    overrides = ""
    for n in we_paths:
        if n.endswith(".rels"):
            continue
        ctype = CT_TASKPANES if n.endswith("taskpanes.xml") else CT_WEBEXTENSION
        if f'PartName="/{n}"' not in ct:
            overrides += f'<Override PartName="/{n}" ContentType="{ctype}"/>'
    items["[Content_Types].xml"] = ct.replace("</Types>", overrides + "</Types>").encode("utf-8")

    # Package-level relationship to taskpanes.xml, mirroring where the donor holds it.
    taskpanes = next((n for n in we_paths if n.endswith("/taskpanes.xml")), None)
    if taskpanes is None:
        sys.exit("error: donor has no taskpanes.xml — save the donor with the Singlepane pane open")
    donor_rels = dz.read("_rels/.rels").decode("utf-8")
    if TASKPANES_REL_TYPE not in donor_rels:
        sys.exit("error: donor _rels/.rels lacks the webextensiontaskpanes relationship — unexpected donor layout")
    rels = items["_rels/.rels"].decode("utf-8")
    used = [int(i) for i in re.findall(r'Id="rId(\d+)"', rels)]
    rid = max(used, default=0) + 1
    rels = rels.replace(
        "</Relationships>",
        f'<Relationship Id="rId{rid}" Type="{TASKPANES_REL_TYPE}" Target="{taskpanes}"/></Relationships>',
    )
    items["_rels/.rels"] = rels.encode("utf-8")

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in order:
            zout.writestr(n, items[n])
        for n in items:
            if n not in order:
                zout.writestr(n, items[n])

    nvars = len(store["variables"])
    print(f"wrote {out_path}: embedded {STORE_KEY} ({nvars} variables) into {store_part}, "
          f"auto-open pane enabled, host={prefix}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="generated .pptx/.docx with <<tags>>")
    ap.add_argument("donor", nargs="?", help="same-type file previously saved with the add-in")
    ap.add_argument("store", nargs="?", help="sp_docs_store JSON file")
    ap.add_argument("-o", "--output", help="output path (default: overwrite target)")
    ap.add_argument("--validate-only", metavar="STORE_JSON", help="validate a store JSON and exit")
    args = ap.parse_args()

    store_path = args.validate_only or args.store
    if not store_path:
        ap.error("store.json required (or use --validate-only)")
    with open(store_path) as f:
        store = json.load(f)
    errors, warnings = validate_store(store)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        sys.exit(f"{len(errors)} validation error(s) — nothing written")
    print(f"store OK: {len(store.get('variables', []))} variables"
          + (f", {len(warnings)} warning(s)" if warnings else ""))

    if args.validate_only:
        return
    if not (args.target and args.donor):
        ap.error("target and donor are required to graft")
    graft(args.target, args.donor, store, args.output or args.target)


if __name__ == "__main__":
    main()
