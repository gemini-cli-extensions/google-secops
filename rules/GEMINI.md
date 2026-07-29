# Google SecOps Extension

This repository contains the **Google SecOps Extension**, providing specialized skills and tools for security operations.

This is not an officially supported Google product.

This project is not eligible for the Google Open Source Software Vulnerability Rewards Program.

## Overview

This extension packages setup and key security workflows into [skills](https://agentskills.io/specification). 

Crucially, it **automatically configures the [Google Cloud Remote MCP Server for SecOps](https://security.googlecloudcommunity.com/community-blog-42/google-cloud-remote-mcp-server-for-secops-6559)**. This means:
*   **No Local Tools**: You don't need to install or manage local Python environments for standard tools.
*   **Enterprise Ready**: Connects directly to Google's managed infrastructure for SecOps.
*   **Adaptive**: While it defaults to the Remote server, it can fallback to local tools if needed.

## Prerequisites

1.  **Install Gemini CLI (Preview)**:
    ```bash
    npm install -g @google/gemini-cli@preview
    ```

2.  **Google Cloud Authentication**: Ensure you are authenticated with Google Cloud and have set a quota project:
    ```bash
    gcloud auth application-default login
    gcloud auth application-default set-quota-project <YOUR_PROJECT_ID>
    ```

3.  **Enable MCP Service**: You must enable the Chronicle MCP service in your Google Cloud project:
    ```bash
    gcloud beta services mcp enable chronicle.googleapis.com/mcp --project=<YOUR_PROJECT_ID>
    ```

4.  **GUI Login Requirement**: You MUST have logged into the Google SecOps GUI at least once before using the API/MCP server.

5.  **Enable Skills**: Ensure your `~/.gemini/settings.json` has `experimental.skills` enabled:
    ```json
    {
      "security": {
        "auth": {
          "selectedType": "gemini-api-key"
        }
      },
      "general": {
        "previewFeatures": true
      },
      "experimental": {
        "skills": true,
        "extensionConfig": true
      }
    }
    ```

## Installation

### Option 1: Install directly from GitHub (Fastest)

You can install this extension directly without cloning:

```bash
gemini extensions install https://github.com/gemini-cli-extensions/google-secops
```

### Option 2: Clone and Install Locally (Best for Development)

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/gemini-cli-extensions/google-secops.git
    cd google-secops
    ```

2.  **Install the extension**:
    ```bash
    gemini extensions install .
    ```

### Option 3: Install as an Antigravity Plugin (via `just`)

If you have `just` installed, you can use the provided recipes:
```bash
# Install globally for Antigravity Desktop
just install-agy-dsk

# Or install for all Antigravity runtimes (Desktop, IDE, CLI)
just install-agy-all

# Uninstall (supports specific flavors like uninstall-agy-dsk or all flavors via uninstall-agy)
just uninstall-agy
```

### Updating and Uninstalling

*   **Update**: `gemini extensions update google-secops`
*   **Uninstall**: `gemini extensions uninstall google-secops`

## Loading as a Plugin (Antigravity, Claude Code & OpenAI Codex)

You can load this extension directly as a plugin in **Antigravity**, **Claude Code**, and **OpenAI Codex**.

### Antigravity Integration
To load the extension in Antigravity, place or symlink the repository folder inside one of these directories:
*   **Workspace-Level**: Place in `.agents/plugins/google-secops/` (active only for the current workspace).
*   **Global-Level**: Place in `~/.gemini/config/plugins/google-secops/` (active across all workspaces).

Antigravity will automatically discover the `plugin.json` manifest file at the root of the directory and expose all SecOps skills, guidelines, and rules.

### Claude Code Integration
To load the extension in Claude Code:
*   **Workspace-Level**: Place or symlink the repository folder inside `.claude/plugins/google-secops/` at the root of your workspace.
*   **Global-Level**: Run the `claude` command with the plugin directory flag:
    ```bash
    claude --plugin-dir /path/to/google-secops
    ```

Claude Code will automatically discover the `.claude-plugin/plugin.json` manifest and expose all skills under the `/google-secops:` namespace.

### OpenAI Codex Integration
To load the extension in Codex:
*   **Workspace-Level / Manual Integration**: Place or symlink the repository folder inside `.codex-plugin/` at the root of your workspace or custom plugin marketplace directory.

Codex will automatically discover the `.codex-plugin/plugin.json` manifest file at the root of the directory and register all SecOps skills.


## Post-Installation

### 1. Configuration

During installation under Antigravity / Gemini CLI, you will be prompted for several parameters:

*   `PROJECT_ID`: Your Google Cloud Project ID (not number).
*   `CUSTOMER_ID`: Your Chronicle Customer UUID4.
*   `REGION`: Your Chronicle Region (e.g., `us`, `europe-west1`).
*   `SERVER_URL`: The regional MCP endpoint (e.g., `https://chronicle.us.rep.googleapis.com/mcp`).

> **Note**: For Antigravity, these values are persisted in `~/.gemini/extensions/google-secops/.env`. You can edit this file at any time to update your configuration.

#### Claude Code Configuration
For Claude Code, the required environment variables (`PROJECT_ID`, `CUSTOMER_ID`, `REGION`, `SERVER_URL`) should be set in your shell environment or loaded using tools like `direnv` or a `.env` file in the current working directory.

### 2. Verify Skills

Run the following command to ensure the skills are loaded:

```bash
/skills list
```

You should see `secops-triage`, etc., in the list.

## Usage

### Available Skills

*   **Alert Triage** (`secops-triage`)
    *   *Trigger*: "Triage alert [ID]", "Analyze case [ID]"
    *   *Function*: Orchestrates a Tier 1 triage workflow (deduplication, enrichment, classification).
*   **Investigation** (`secops-investigate`)
    *   *Trigger*: "Investigate case [ID]", "Deep dive on [Entity]"
    *   *Function*: Guides deep-dive investigations using specialized runbooks.
*   **Threat Hunting** (`secops-hunt`)
    *   *Trigger*: "Hunt for [Threat]", "Search for TTP [ID]"
    *   *Function*: Assists in proactive threat hunting by generating hypotheses and constructing complex UDM queries.
*   **Cases** (`secops-cases`)
    *   *Trigger*: "List cases", "Show recent cases", "/secops:cases"
    *   *Function*: Lists recent SOAR cases to verify connectivity.
*   **Detection Engineering** (`secops-detection-engineering`)
    *   *Trigger*: "Evaluate detection coverage", "Generate TDOs from blog", "Check rule coverage for TTP"
    *   *Function*: Automates the end-to-end detection engineering workflow (threat intell extraction, TDO generation, synthetic event simulation, coverage evaluation, and YARA-L rule creation).

### Custom Commands

Use these shortcuts for common tasks:

*   `/secops:triage <ALERT_ID>`
*   `/secops:investigate <CASE_ID>`
*   `/secops:hunt <THREAT>`
*   `/secops:cases`
*   `/secops:detection-engineering <THREAT_INTEL>`

## Known Issues

* **Regional Endpoints**: If the `SERVER_URL` requires regionalization, ensure you use the correct endpoint from the [official documentation](https://docs.cloud.google.com/chronicle/docs/secops/use-google-secops-mcp).

Known-good values for Regional Endpoints (REP):
* `https://chronicle.us-east1.rep.googleapis.com/mcp`
* `https://chronicle.europe-west1.rep.googleapis.com/mcp`
* `https://chronicle.us.rep.googleapis.com/mcp` (Multi-Regional)

## References
* [Google Cloud Remote MCP Server for SecOps Blog](https://security.googlecloudcommunity.com/community-blog-42/google-cloud-remote-mcp-server-for-secops-6559)
* [Agent Skills Specification](https://agentskills.io/specification)
* [Gemini CLI Documentation](https://geminicli.com)
* [Antigravity Skills](https://antigravity.google/docs/skills)
* [Use the Google SecOps MCP server](https://docs.cloud.google.com/chronicle/docs/secops/use-google-secops-mcp)
