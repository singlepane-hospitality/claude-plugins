#!/usr/bin/env python3
"""Make SP.* add-in formulas written by openpyxl/xlsxwriter calculate on open in
Excel instead of showing #NAME? (or =@SP...) until each cell is re-entered.

Excel binds Office.js custom functions by a mangled internal name persisted in the
file XML. Verified against a real Excel-for-Mac save of a working Singlepane cell:

    <c r="C20" cm="1"><f t="array" ref="C20">_xldudf_SP_FINANCIALS(...)</f></c>

i.e. prefix `_xldudf_`, namespace dot replaced by underscore, cell marked as a
dynamic-array formula (cm="1", t="array") with the XLDAPR metadata part present.
A bare `SP.FINANCIALS(...)` in the XML never binds to the add-in, which is why
F2+Enter (a live re-parse) was the only thing that fixed it. This script rewrites
every SP.* formula cell into that exact persisted form.

Usage: python3 fix_sp_formulas.py workbook.xlsx [more.xlsx ...]
Rewrites each file in place.
"""
import re
import shutil
import sys
import tempfile
import zipfile

METADATA_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<metadata xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
    'xmlns:xlda="http://schemas.microsoft.com/office/spreadsheetml/2017/dynamicarray">'
    '<metadataTypes count="1">'
    '<metadataType name="XLDAPR" minSupportedVersion="120000" copy="1" pasteAll="1" '
    'pasteValues="1" merge="1" splitFirst="1" rowColShift="1" clearFormats="1" '
    'clearComments="1" assign="1" coerce="1" cellMeta="1"/>'
    '</metadataTypes>'
    '<futureMetadata name="XLDAPR" count="1">'
    '<bk><extLst><ext uri="{bdbb8cdc-fa1e-496e-a857-3c3f30c029c3}">'
    '<xlda:dynamicArrayProperties fDynamic="1" fCollapsed="0"/>'
    '</ext></extLst></bk>'
    '</futureMetadata>'
    '<cellMetadata count="1"><bk><rc t="1" v="0"/></bk></cellMetadata>'
    '</metadata>'
)

SP_CALL = re.compile(r'(?:^|[^A-Za-z0-9_.])(?:_xldudf_SP_|SP\.)[A-Za-z_]+\s*\(')
SP_NAME = re.compile(r'(?<![A-Za-z0-9_.])SP\.([A-Za-z_]+)(\s*\()')
# openpyxl writes formula cells as <c r="C20" s="5"><f>SP...(...)</f>...</c>
CELL_F = re.compile(r'<c ([^>/]*)>((?:<[^/f][^>]*/>)*)<f(| [^>]*)>([^<]*)</f>')


def fix_sheet(xml: str) -> tuple[str, int]:
    count = 0

    def repl(m):
        nonlocal count
        attrs, pre, f_attrs, formula = m.groups()
        if not SP_CALL.search(formula):
            return m.group(0)
        # Excel's persisted form for Office.js UDFs: SP.FUNC( -> _xldudf_SP_FUNC(
        new_formula = SP_NAME.sub(r'_xldudf_SP_\1\2', formula)
        ref = re.search(r'r="([A-Z]+\d+)"', attrs)
        if not ref:
            return m.group(0)
        if new_formula == formula and 'cm=' in attrs and 't="array"' in f_attrs:
            return m.group(0)  # already fully fixed
        if 'cm=' not in attrs:
            attrs = attrs.rstrip() + ' cm="1"'
        if 't="array"' not in f_attrs:
            f_attrs = f' t="array" ref="{ref.group(1)}"'
        count += 1
        return f'<c {attrs}>{pre}<f{f_attrs}>{new_formula}</f>'

    return CELL_F.sub(repl, xml), count


def fix_workbook(path: str) -> int:
    total = 0
    with zipfile.ZipFile(path) as zin:
        names = zin.namelist()
        items = {n: zin.read(n) for n in names}

    for name in list(items):
        if re.fullmatch(r'xl/worksheets/sheet\d+\.xml', name):
            xml, n = fix_sheet(items[name].decode('utf-8'))
            items[name] = xml.encode('utf-8')
            total += n

    if total and 'xl/metadata.xml' not in items:
        items['xl/metadata.xml'] = METADATA_XML.encode('utf-8')
        ct = items['[Content_Types].xml'].decode('utf-8')
        if 'metadata.xml' not in ct:
            ct = ct.replace('</Types>',
                            '<Override PartName="/xl/metadata.xml" ContentType='
                            '"application/vnd.openxmlformats-officedocument.'
                            'spreadsheetml.sheetMetadata+xml"/></Types>')
            items['[Content_Types].xml'] = ct.encode('utf-8')
        rels = items['xl/_rels/workbook.xml.rels'].decode('utf-8')
        if 'metadata.xml' not in rels:
            used = [int(i) for i in re.findall(r'Id="rId(\d+)"', rels)]
            rid = max(used, default=0) + 1
            rels = rels.replace('</Relationships>',
                                f'<Relationship Id="rId{rid}" Type="http://schemas.'
                                'openxmlformats.org/officeDocument/2006/relationships/'
                                'sheetMetadata" Target="metadata.xml"/></Relationships>')
            items['xl/_rels/workbook.xml.rels'] = rels.encode('utf-8')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            for name in names:
                zout.writestr(name, items[name])
            for name in items:
                if name not in names:
                    zout.writestr(name, items[name])
        shutil.move(tmp.name, path)
    return total


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        n = fix_workbook(p)
        print(f'{p}: marked {n} SP.* formula cell(s) as dynamic-array')
