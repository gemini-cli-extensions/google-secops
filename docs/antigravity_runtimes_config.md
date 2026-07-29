# Antigravity Runtimes & Configuration Reference

This document details the directory locations, configuration file paths, and runtime behaviors across the three Google Antigravity product surfaces:
- **Antigravity 2.0 (Desktop Standalone App)**
- **Antigravity IDE (Visual Studio Code Extension / IDE Integration)**
- **Antigravity CLI (`agy`)**

All information in this document is sourced directly from official Google Developer documentation (`antigravity.google` and `developers.google.com`).

---

## Quick Comparison Matrix

The table below summarizes the official global and workspace paths for each runtime environment as documented in the Google Developer Knowledge corpus.

| Feature / Location | Antigravity 2.0 (Desktop Standalone App) | Antigravity IDE | Antigravity CLI (`agy`) |
| :--- | :--- | :--- | :--- |
| **Primary Interface** | Visual desktop application | VS Code / IDE extension | Terminal TUI |
| **Global Plugin Bundle Path** | `~/.gemini/config/plugins/<plugin-name>/`<br>*(contains `plugin.json`, `skills/`, `mcp_config.json`)* | `~/.gemini/config/plugins/<plugin-name>/` | Not applicable (Plugins convert to CLI skills) |
| **Workspace Plugin Bundle Path** | `<workspace-root>/.agents/plugins/<plugin-name>/` | `<workspace-root>/.agents/plugins/<plugin-name>/` | Not applicable |
| **Global Standalone Skills Path** | `~/.gemini/config/skills/<skill-folder>/` | `~/.gemini/antigravity/skills/<skill-folder>/`<br>*(or `~/.gemini/antigravity-ide/skills/`)* | `~/.gemini/antigravity-cli/skills/` |
| **Workspace Standalone Skills Path** | `<workspace-root>/.agents/skills/<skill-folder>/` | `<workspace-root>/.agents/skills/<skill-folder>/` | `<workspace-root>/.agents/skills/` |
| **Global MCP Config Path** | `~/.gemini/config/plugins/<plugin-name>/mcp_config.json`<br>*(plugin-scoped)* or `~/.gemini/config/mcp_config.json`<br>*(system-wide)* | `~/.gemini/antigravity/mcp_config.json`<br>*(or `~/.gemini/config/mcp_config.json`)* | `~/.gemini/antigravity-cli/mcp_config.json` |
| **Workspace MCP Config Path** | `<workspace-root>/.agents/plugins/<plugin-name>/mcp_config.json`<br>*(plugin-scoped)* or `<workspace-root>/.agents/mcp_config.json` | `<workspace-root>/.agents/mcp_config.json` | `<workspace-root>/.agents/mcp_config.json` |

---

## Key Differences & Overlapping Paths

### 1. Plugin Bundling vs. Standalone Skills (Desktop Parity)
A critical distinction in Antigravity Desktop (`agy-dsk`) is the difference between standalone skill scripts and structured plugin bundles:
- **Plugin Bundles (Recommended)**: When a plugin manifest (`plugin.json`) is deployed to `~/.gemini/config/plugins/<plugin-name>/` (global) or `<workspace-root>/.agents/plugins/<plugin-name>/` (project, with `<workspace-root>/_agents/plugins/` as an alternate workspace path), Antigravity Desktop automatically scans and registers all skills inside the plugin's `skills/` subdirectory. This keeps plugin skills and dependencies isolated from global namespaces.
- **Standalone Skills**: For IDE and CLI flavors (or simple standalone scripts), skills are installed directly into flavor-specific profile directories (`~/.gemini/antigravity/skills/` or `~/.gemini/antigravity-cli/skills/`).
- **Workspace Parity**: All three runtimes standardize on `<workspace-root>/.agents/skills/` for standalone project-level skills (maintaining backward compatibility for legacy `.agent/skills/` singular syntax).

### 2. Model Context Protocol (MCP) Resolution & Isolation
- **Plugin-Scoped MCP Config**: In Antigravity Desktop, plugins define their own `mcp_config.json` directly inside their plugin root (`~/.gemini/config/plugins/<plugin-name>/mcp_config.json`). Antigravity automatically loads these servers when the plugin is active, avoiding global `~/.gemini/config/mcp_config.json` namespace pollution.
- **Profile-Scoped MCP Config**: For IDE and CLI flavors, global MCP configurations are merged directly into their profile directories (`~/.gemini/antigravity/mcp_config.json` or `~/.gemini/antigravity-cli/mcp_config.json`).
- **OAuth Token Cache**: Cached OAuth access tokens for `google_credentials` auth provider endpoints are stored in `~/.gemini/antigravity/mcp_oauth_tokens.json`. Expired tokens are refreshed automatically; invalid or corrupted tokens can be pruned from this file during troubleshooting.
- **Safe Configuration Merging**: When automated deployment tools (like `scripts/install.py`) install or update MCP configs, they use parameterized template variables (`${SERVER_URL}`, `${PROJECT_ID}`) and perform safe dictionary merges. This ensures user-configured headers (such as `x-goog-user-project`) are preserved across updates without clobbering existing configuration files.

### 3. Cross-Page Documentation Discrepancies & Legacy Migration
- **Documentation Resolution Hierarchy**: General overview pages (such as `/docs/skills`) describe a single global skills path (`~/.gemini/config/skills/`), but product-surface specific guides (`/docs/ide/skills` and `/docs/cli/plugins`) override this with surface-specific profile paths (`~/.gemini/antigravity/skills/` and `~/.gemini/antigravity-cli/skills/`). The installer follows surface-specific paths to ensure proper isolation.
- Legacy Gemini CLI workspace skills (`.gemini/skills/`) must be relocated to `.agents/skills/`.
- Legacy Gemini CLI extensions can be loaded natively as plugins by adding a `plugin.json` manifest alongside `gemini-extension.json`.

---

## Official Documentation References

The data in this document is cited directly from official Google Developer documentation:

1. **Agent Skills & Directory Specs**:
   - [Google Antigravity Skills Overview](https://antigravity.google/docs/skills)
   - [Google Antigravity IDE Skills Guide](https://antigravity.google/docs/ide/skills)
2. **MCP Configuration Specs**:
   - [Google Antigravity MCP Documentation](https://antigravity.google/docs/mcp)
   - [Google Workspace MCP Setup Guide](https://developers.google.com/workspace/guides/universal-search-mcp)
3. **Plugin Architecture & CLI Migration**:
   - [Google Antigravity Plugins Spec](https://antigravity.google/docs/plugins)
   - [Google Antigravity CLI Overview & Migration](https://antigravity.google/docs/cli/overview)
   - [Google Antigravity CLI Using & Configuration](https://antigravity.google/docs/cli/using)
   - [Google Antigravity CLI Plugins & Skills](https://antigravity.google/docs/cli/plugins)
