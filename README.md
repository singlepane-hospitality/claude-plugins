# Singlepane Claude Plugins

Official [Singlepane](https://www.singlepaneapp.com) plugin marketplace for Claude.

## Plugins

### singlepane-excel-modeling

Teaches Claude to build Excel financial models with the Singlepane Excel add-in's
`SP.*` functions — summary P&Ls and department schedules on canonical USALI layouts,
variance reports, portfolio rollups, STR comp-set dashboards, and OTB/pace reports.
Requires the Singlepane Excel add-in (and a Singlepane login) for the workbooks to
populate with data.

## Install

In Claude Code or the Claude desktop app:

```
/plugin marketplace add singlepane-hospitality/claude-plugins
/plugin install singlepane-excel-modeling@singlepane
```

When adding the marketplace, Claude shows a standard notice about third-party
sources — that's expected for any non-Anthropic marketplace.

## Updates

```
/plugin update singlepane-excel-modeling
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

Org admins can instead upload the packaged skill directly: download
`singlepane-excel-modeling.skill` from this repo's
[latest release](https://github.com/singlepane-hospitality/claude-plugins/releases/latest)
and add it under organization skill settings. Note this copy does not auto-update —
re-upload when a new release is published.
