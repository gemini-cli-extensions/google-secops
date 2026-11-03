# Antigravity Configuration & Installation Locations Guide

This document summarizes the installation methods, configuration paths, workspace hierarchy, and caching locations across the three flavors of Google Antigravity: **Antigravity 2.0 (Desktop App)**, **Antigravity IDE**, and **Antigravity CLI (`agy`)**.

---

## Quick Reference: Path Comparison

| Resource / Scope | Antigravity 2.0 (Desktop App) | Antigravity IDE (VS Code Fork) | Antigravity CLI (`agy`) |
| :--- | :--- | :--- | :--- |
| **Installation** | Desktop installer (`https://antigravity.google`) | Standalone IDE installer | `curl -fsSL https://antigravity.google/cli/install.sh \| bash` |
| **CLI / App Settings** | In-App Settings Panel / UI | Settings UI (`Cmd+,` / `Ctrl+,`) | `~/.gemini/antigravity-cli/settings.json` |
| **Global MCP Config** | `~/.gemini/config/mcp_config.json` | `~/.gemini/config/mcp_config.json` | `~/.gemini/config/mcp_config.json` |
| **Global Skills** | `~/.gemini/config/skills/` | `~/.gemini/config/skills/` | `~/.gemini/config/skills/` |
| **Global Plugins** | `~/.gemini/config/plugins/` | `~/.gemini/config/plugins/` | `~/.gemini/config/plugins/` |
| **Global Rules** | `~/.gemini/config/rules/*.md`, `GEMINI.md` | `~/.gemini/config/rules/*.md`, `GEMINI.md` | `~/.gemini/config/rules/*.md`, `GEMINI.md` |
| **Project Customizations Root** | `<workspace-root>/.agents/` | `<workspace-root>/.agents/` | `<workspace-root>/.agents/` |
| **Project MCP Config** | `<workspace-root>/.agents/mcp_config.json` | `<workspace-root>/.agents/mcp_config.json` | `<workspace-root>/.agents/mcp_config.json` |
| **Project Skills** | `<workspace-root>/.agents/skills/` | `<workspace-root>/.agents/skills/` | `<workspace-root>/.agents/skills/` |
| **Project Plugins** | `<workspace-root>/.agents/plugins/` | `<workspace-root>/.agents/plugins/` | `<workspace-root>/.agents/plugins/` |
| **Project Rules** | `GEMINI.md`, `AGENTS.md`, `.agents/rules/` | `GEMINI.md`, `AGENTS.md`, `.agents/rules/` | `GEMINI.md`, `AGENTS.md`, `.agents/rules/` |
| **App State / Artifacts** | `~/.gemini/antigravity/` | `~/.gemini/antigravity-ide/` | `~/.gemini/antigravity-cli/` |
| **MCP Tool Cache** | `~/.gemini/antigravity/mcp/` | `~/.gemini/antigravity-ide/mcp/` | `~/.gemini/antigravity-cli/mcp/` |

---

## 1. Antigravity 2.0 (Desktop Application)

Antigravity 2.0 is the standalone desktop command center designed for autonomous agent orchestration, parallel subagents, and background missions.

### Installation
* Downloaded and installed as a standalone desktop application via [antigravity.google](https://antigravity.google).
* OS-specific application data directories:
  * **Linux:** `~/.config/Antigravity/` and `~/.local/share/Antigravity/`
  * **macOS:** `~/Library/Application Support/Antigravity/`
  * **Windows:** `%APPDATA%\Antigravity\` and `%LOCALAPPDATA%\Antigravity\`

### Global Configurations
* **Base Global Directory:** `~/.gemini/`
* **MCP Server Definitions:** `~/.gemini/config/mcp_config.json`
* **Global Customizations & Skills:** `~/.gemini/config/skills/<skill_name>/SKILL.md`
* **Global Plugins:** `~/.gemini/config/plugins/<plugin_name>/`
* **Internal Application State & Artifacts:** `~/.gemini/antigravity/` (stores session transcripts, artifacts, knowledge bases)
* **MCP Server Schema Cache:** `~/.gemini/antigravity/mcp/<server_name>/` *(Note: If an MCP server is uninstalled, delete its cache here to prevent stale tool listings).*

### Project / Workspace Configurations
* **Workspace Customizations Directory:** `<project-root>/.agents/`
* **Workspace MCP Servers:** `<project-root>/.agents/mcp_config.json`
* **Workspace Skills:** `<project-root>/.agents/skills/<skill_name>/SKILL.md`
* **Workspace Rules:** `<project-root>/GEMINI.md`, `<project-root>/AGENTS.md`, `<project-root>/.agents/rules/*.md`

### Management
* Configure via the GUI **Settings** panel or the **Agent Panel** (`...` > **Manage MCP Servers** > **View raw config**).

---

## 2. Antigravity IDE (VS Code Fork)

Antigravity IDE provides an in-editor agentic programming experience built directly on a VS Code-compatible foundation.

### Installation
* Installed as a dedicated desktop IDE application.

### Global Configurations
* **Base Global Directory:** `~/.gemini/`
* **Global MCP Servers:** `~/.gemini/config/mcp_config.json`
* **Global Skills:** `~/.gemini/config/skills/`
* **Global Plugins:** `~/.gemini/config/plugins/`
* **IDE Internal State & Cache:** `~/.gemini/antigravity-ide/`
* **IDE MCP Server Cache:** `~/.gemini/antigravity-ide/mcp/<server_name>/`

### Project / Workspace Configurations
* **Project Customizations Directory:** `<project-root>/.agents/`
* **Project MCP Servers:** `<project-root>/.agents/mcp_config.json`
* **Project Skills:** `<project-root>/.agents/skills/`
* **Project Rules:** `GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md`

### Management
* Managed via the IDE **Settings Editor** (`Cmd+,` / `Ctrl+,` or Gear Icon > **Settings** > **Customizations**).
* Project-specific configurations can be set via project settings in the sidebar.

---

## 3. Antigravity CLI (`agy`)

The Antigravity CLI is a fast, terminal-based Go application that replaces the legacy Gemini CLI for headless execution, automated evaluations, and terminal-first workflows.

### Installation
```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

### Global Configurations
* **CLI Preferences & Settings:** `~/.gemini/antigravity-cli/settings.json` (controls CLI-specific settings like theme, default models, sandbox flags).
* **Global MCP Server Configuration:** `~/.gemini/config/mcp_config.json` *(Dedicated MCP config file separated from `settings.json`).*
* **Global Skills:** `~/.gemini/config/skills/`
* **Global Plugins:** `~/.gemini/config/plugins/`
* **CLI MCP Cache:** `~/.gemini/antigravity-cli/mcp/`

### Project / Workspace Configurations
* **Workspace Customizations Directory:** `<project-root>/.agents/`
* **Workspace MCP Servers:** `<project-root>/.agents/mcp_config.json`
* **Workspace Skills:** `<project-root>/.agents/skills/`
* **Workspace Plugins:** `<project-root>/.agents/plugins/`
* **Workspace Rules:** `GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md`

### Managing & Migrating
* **Interactive Settings:** Run `/config`, `/settings`, or `/plugin` within an `agy` session to open interactive configuration menus (including plugin MCP `variables` setup).
* **CLI Flags:** Override settings per invocation (e.g., `agy --sandbox`, `agy --model <name>`).
* **Legacy Gemini Extension Migration:** Run `agy plugin import gemini` to automatically scan `~/.gemini/extensions/` and migrate them to `~/.gemini/config/plugins/`.
* **Plugin Commands:**
  * `agy plugin validate <dir> --strict`
  * `agy plugin list`
  * `agy plugin install <source>`
  * `agy plugin enable <name>` / `agy plugin disable <name>`

---

## Antigravity Plugin Directory Structure

For packages intended as Antigravity Plugins (and backwards-compatible Gemini CLI extensions), every skill directory name must match the `name` field in its `SKILL.md` frontmatter, and plugin-scoped always-on rules reside in `rules/AGENTS.md`:

```text
google-secops/
├── plugin.json                 # Antigravity plugin manifest (no agent-plugins.org $schema when using MCP variables)
├── mcp_config.json             # Managed remote MCP server definition with interactive variables
├── assets/
│   └── logo.svg                # Square vector plugin icon
├── rules/                      # Plugin-scoped rules
│   └── AGENTS.md               # Plain Markdown always-on operational rules
├── skills/                     # Plugin skills (folder name matches SKILL.md name)
│   ├── secops-cases/SKILL.md
│   ├── secops-detection-engineering/SKILL.md
│   ├── secops-hunt/SKILL.md
│   ├── secops-investigate/SKILL.md
│   └── secops-triage/SKILL.md
├── gemini-extension.json       # Gemini CLI extension manifest (legacy compatibility)
├── README.md
└── TOOL_MAPPING.md
```
