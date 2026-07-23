# Singlepane for Claude

Official [Singlepane](https://www.singlepaneapp.com) plugin marketplace for Claude.

## The `singlepane` plugin

One plugin, two pieces:

- **Singlepane MCP connector** (`https://ai.singlepaneapp.com/mcp`) — lets Claude look
  up your hotels and query Singlepane data directly. On first use you'll be prompted
  to sign in to Singlepane to authorize the connection.
- **Excel modeling skill** — teaches Claude to build Excel financial models with the
  Singlepane Excel add-in's `SP.*` functions: summary P&Ls and department schedules on
  canonical USALI layouts, variance reports, portfolio rollups, STR comp-set
  dashboards, and OTB/pace reports. Requires the Singlepane Excel add-in (and a
  Singlepane login) for workbooks to populate with data.

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

## claude.ai (web) users

Org admins can instead upload the packaged Excel-modeling skill directly: download
`singlepane-excel-modeling.skill` from this repo's
[latest release](https://github.com/singlepane-hospitality/claude-plugins/releases/latest)
and add it under organization skill settings, and add the Singlepane connector under
connector settings. Note the uploaded skill does not auto-update — re-upload when a
new release is published.
