# Google SecOps Extension

This repository contains the **Google SecOps Extension**, providing specialized skills and tools for security operations.

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
gemini extensions install github:dandye/secops-gemini-extension
```

### Option 2: Clone and Install Locally (Best for Development)

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/dandye/secops-gemini-extension.git
    cd secops-gemini-extension
    ```

2.  **Install the extension**:
    ```bash
    gemini extensions install .
    ```

### Updating and Uninstalling

*   **Update**: `gemini extensions update google-secops`
*   **Uninstall**: `gemini extensions uninstall google-secops`

## Post-Installation

### 1. Configuration

During installation, you will be prompted for several parameters:

*   `PROJECT_ID`: Your Google Cloud Project ID.
*   `CUSTOMER_ID`: Your Chronicle Customer UUID.
*   `REGION`: Your Chronicle Region (e.g., `us`, `europe-west1`).
*   `SERVER_URL`: The regional MCP endpoint (e.g., `https://chronicle.us.rep.googleapis.com/mcp`).

> **Note**: These values are persisted in `~/.gemini/extensions/google-secops/.env`. You can edit this file at any time to update your configuration.

### 2. Verify Skills

Run the following command to ensure the skills are loaded:

```bash
/skills list
```

You should see `secops-setup-antigravity`, `secops-triage`, etc., in the list.

## Usage

### Available Skills

*   **Setup Assistant** (`secops-setup-antigravity`)
    *   *Trigger*: "Help me set up Antigravity", "Configure Antigravity for SecOps"
    *   *Function*: Helps configure Antigravity to also use the Remote MCP Server.
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

### Custom Commands

Use these shortcuts for common tasks:

*   `/secops:triage <ALERT_ID>`
*   `/secops:investigate <CASE_ID>`
*   `/secops:hunt <THREAT>`
*   `/secops:cases`

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
