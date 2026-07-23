# Singlepane for Claude

Official [Singlepane](https://www.singlepaneapp.com) plugin marketplace for Claude.

## The `singlepane` plugin

One plugin, three pieces:

- **Singlepane MCP connector** (`https://ai.singlepaneapp.com/mcp`) — lets Claude look
  up your hotels and query Singlepane data directly. On first use you'll be prompted
  to sign in to Singlepane to authorize the connection.
- **Excel modeling skill** — teaches Claude to build Excel financial models with the
  Singlepane Excel add-in's `SP.*` functions: summary P&Ls and department schedules on
  canonical USALI layouts, variance reports, portfolio rollups, STR comp-set
  dashboards, and OTB/pace reports. Requires the Singlepane Excel add-in (and a
  Singlepane login) for workbooks to populate with data.
- **Docs skill (PowerPoint & Word)** — teaches Claude to build slide decks and
  documents whose numbers refresh through the Singlepane Docs add-in: `<<Variable>>`
  tags in slides/paragraphs/tables backed by financials, STR, and OTB query
  variables — monthly performance decks, board and owner reports, lender updates.
  Requires the Singlepane Docs add-in (and a Singlepane login) for documents to
  populate with data.

More skills will ship in this same plugin over time — installed users get them
automatically on update.

## Install

In Claude Code or the Claude desktop app:

```
/plugin marketplace add singlepane-hospitality/claude-plugins
/plugin install singlepane@singlepane
```

When adding the marketplace, Claude shows a standard notice about third-party
sources — that's expected for any non-Anthropic marketplace.

## Updates

```
/plugin update singlepane
```

Claude also periodically refreshes marketplaces on its own.

## For IT administrators (managed/enterprise deployments)

If your organization restricts plugin marketplaces (`strictKnownMarketplaces` in
Claude Code, `allowedPluginMarketplaces` in Claude Desktop), allowlist:

```
https://github.com/singlepane-hospitality/claude-plugins
```

Organizations can also auto-install or force-install the plugin for all users via
their managed-settings/MDM configuration.

## claude.ai and Microsoft 365 add-in users (Claude for Excel / Word / PowerPoint)

The plugin marketplace above only works in Claude Code and the Claude desktop app. For
every other surface — claude.ai on the web, and the Claude for Excel, Word, and
PowerPoint sidebars — the skills are delivered as uploaded `.skill` files instead.
Skills enabled in a user's claude.ai settings automatically carry into the Microsoft
365 add-ins, so one upload covers all of these surfaces (Claude filters out skills not
relevant to the app it's running in).

**Getting the file** — every merge to `main` republishes fresh builds, and these direct
links always point at the newest one:

- [singlepane-excel-modeling.skill](https://github.com/singlepane-hospitality/claude-plugins/releases/download/latest/singlepane-excel-modeling.skill)
- [singlepane-docs.skill](https://github.com/singlepane-hospitality/claude-plugins/releases/download/latest/singlepane-docs.skill)

A `.skill` file is just a zip, so sharing the link or emailing the downloaded file
both work.

**Installing it:**

- **Individual users**: claude.ai → Settings → Capabilities → Skills → upload the
  `.skill` file.
- **Org admins**: upload once under organization skill settings to enable it for all
  users, and add the Singlepane connector under connector settings.

Two caveats: uploaded skills do not auto-update — re-upload when new builds are
published — and the Singlepane MCP connector is not bundled inside a `.skill`, so
connect it separately if Claude should query Singlepane data directly (inside the
Office add-ins the Singlepane add-ins themselves provide the live data, so the
connector is optional there).
