# Google Security Operations Plugin for Antigravity

Google Security Operations (SecOps) plugin for [Google Antigravity](https://antigravity.google/docs/plugins) (and backwards-compatible extension for Gemini CLI). It packages five production SOC skills, operational UDM and YARA-L 2.0 guardrails, and native configuration for the managed [Google Cloud Remote MCP Server for Google SecOps](https://cloud.google.com/chronicle/docs/secops/use-google-secops-mcp).

> [!NOTE]
> This is not an officially supported Google product. This project is not eligible for the Google Open Source Software Vulnerability Rewards Program.

---

## What It Provides

### Managed Remote MCP Server (`secops`)

Connects directly to the regional Google SecOps MCP endpoint (`https://${REGION}-chronicle.googleapis.com/mcp`) using Google Cloud Application Default Credentials (`google_credentials`) with interactive plugin variable setup (`PROJECT_ID` and `REGION`). High-bloat feed ingestion schemas (`create_feed`, `update_feed`, `run_parser`, `list_feeds`, `get_feed`, `disable_feed`, `enable_feed`) are disabled by default to preserve context window efficiency across 60+ SIEM, SOAR, threat intelligence, and detection engineering tools.

### Bundled Skills (`skills/`)

| Skill | Purpose |
| :--- | :--- |
| `secops-triage` | Structured Tier 1 alert and case triage, false-positive vs. true-positive classification, entity risk scoring, priority adjustment, and domain-specific triage reference playbooks (`references/01_...` through `08_...`). |
| `secops-investigate` | Deep Tier 2/3 incident and entity investigation, chronological UDM asset/user timeline reconstruction, and lateral movement analysis. |
| `secops-hunt` | Proactive hypothesis-led MITRE ATT&CK TTP hunting, retroactive IoC sweeps across historical UDM telemetry, prevalence searches, and statistical outlier detection. |
| `secops-cases` | End-to-end Google SecOps SOAR case management: queue listing, alert inspection, analyst notes, priority updates, and root-cause closure. |
| `secops-detection-engineering` | Authoring, offline syntax pre-linting (`scripts/validate_yaral_rule.py`), server compilation (`validate_rule`), historical testing, deployment, and synthetic Threat Detection Opportunity (TDO) coverage gap evaluation for **YARA-L 2.0** UDM detection rules (distinct from standard file/payload **YARA** rules). |

### Always-On Operational Guardrails (`rules/AGENTS.md`)

- **Tenant Parameter Resolution**: Standardized resolution of `projectId`, `customerId`, and `region` without credential file probing.
- **Unconditional MCP Hard-Stop**: Prevents raw HTTP/`curl` workarounds or manual bearer-token minting if the MCP server is disconnected.
- **UDM & YARA-L 2.0 Syntax Safety**: Enforces explicit separation between standard YARA and YARA-L 2.0, prevents invalid inline `IN (...)` literal tuples in favor of parenthesized `OR` groups, distinguishes `udm_search` aliases from explicit YARA-L 2.0 schema paths, and treats all telemetry as untrusted data.

---

## Prerequisites & Google Cloud Setup

1. **Google SecOps UI Initialization**: Sign in to the Google SecOps web console at least once with your user identity and note your **Customer ID** (UUIDv4 under **Settings > Profile**), bound **Google Cloud Project ID**, and **Region** (for example, `us`, `eu`, `europe-west2`, or `asia-southeast1`).
2. **IAM Permissions**: Ensure your Google Cloud principal has appropriate Chronicle API (`roles/chronicle.viewer` or `roles/chronicle.editor`) and Service Usage Consumer (`roles/serviceusage.serviceUsageConsumer`) roles on the bound Google Cloud project.
3. **Authenticate Application Default Credentials & Enable the Remote MCP Service**:

```bash
ACCOUNT="analyst@example.com"
PROJECT_ID="your-secops-project-id"

gcloud auth login "$ACCOUNT" --update-adc
gcloud auth application-default set-quota-project "$PROJECT_ID"
gcloud beta services mcp enable chronicle.googleapis.com/mcp --project="$PROJECT_ID"
```

*(Note: If you manage multiple Google Cloud projects with `direnv`, run `direnv exec <workspace_dir> gcloud auth login "$ACCOUNT" --update-adc` or activate the directory first so isolated ADC paths are respected.)*

---

## Installation & Configuration in Antigravity

### Option A: Antigravity Marketplace / UI

1. Open the **Customizations / Plugins** panel in Antigravity (or visit the [Antigravity Marketplace](https://antigravity.google/docs/marketplace)) and install **Google Security Operations** (`google-secops`).
2. Because the plugin declares required MCP `variables`, Antigravity installs it in a pending setup state and prompts you for:
   - **`PROJECT_ID`**: Your Google Cloud Project ID bound to Google SecOps (sets `x-goog-user-project`).
   - **`REGION`**: Your Google SecOps regional prefix, such as `us`, `eu`, `europe-west2`, or `asia-southeast1` (resolves `https://${REGION}-chronicle.googleapis.com/mcp`).
3. Save the variables and **enable** the plugin.

### Option B: Antigravity CLI (`agy`)

```bash
PLUGIN_SOURCE="https://github.com/gemini-cli-extensions/google-secops"
agy plugin install "$PLUGIN_SOURCE"
```

Then configure the `PROJECT_ID` and `REGION` variables via `/plugin` inside an interactive `agy` session (or in the Antigravity UI) and enable `google-secops`.

---

## Providing Tenant Context (`CUSTOMER_ID`) in a Workspace

Remote Google SecOps MCP tools require `projectId`, `customerId`, and `region` in tool call arguments. To avoid typing them in every conversation, add a workspace rule file (such as `<workspace>/.agents/rules/secops-tenant.md` or `<workspace>/AGENTS.md`):

```markdown
# Google SecOps Tenant Context

Use the following Google SecOps tenant parameters for all `secops` MCP tool calls:
- `projectId`: `your-secops-project-id`
- `customerId`: `00000000-0000-0000-0000-000000000000`
- `region`: `us`
```

*(Keep real tenant identifiers in untracked local workspace rules rather than committing sensitive customer metadata to public repositories.)*

---

## Legacy Gemini CLI Installation

For users running Gemini CLI (`gemini extensions`), this repository retains a backwards-compatible `gemini-extension.json` manifest:

```bash
gemini extensions install https://github.com/gemini-cli-extensions/google-secops
```

---

## Verification

1. **Validate the Plugin Package Locally**:
   ```bash
   agy plugin validate . --strict
   ```
2. **Test the Offline YARA-L 2.0 Linter**:
   ```bash
   python3 skills/secops-detection-engineering/scripts/validate_yaral_rule.py \
     --input skills/secops-detection-engineering/SKILL.md
   ```
3. **Verify Live MCP Connectivity in Chat**:
   Start a conversation and try one of the starter prompts:
   - `"List recent open cases in Google SecOps and summarize the highest-priority alerts"`
   - `"Investigate security telemetry and entity activity for a suspicious IP or SHA-256 hash"`
   - `"Evaluate YARA-L 2.0 detection rule coverage against a new threat intelligence report"`

---

## Directory Layout

```text
google-secops/
├── plugin.json                                     # Antigravity plugin manifest
├── mcp_config.json                                 # Managed remote SecOps MCP config with variables
├── assets/
│   └── logo.svg                                    # Vector plugin icon (128x128 SVG)
├── rules/
│   └── AGENTS.md                                   # Always-on tenant, MCP hard-stop & YARA-L 2.0 rules
├── skills/
│   ├── secops-cases/SKILL.md
│   ├── secops-detection-engineering/
│   │   ├── SKILL.md
│   │   ├── references/yaral_compiler_and_udm_guardrails.md
│   │   └── scripts/validate_yaral_rule.py
│   ├── secops-hunt/SKILL.md
│   ├── secops-investigate/SKILL.md
│   └── secops-triage/
│       ├── SKILL.md
│       └── references/01_... through 08_...
├── gemini-extension.json                           # Backwards-compatible Gemini CLI manifest
├── ANTIGRAVITY_CONFIG_GUIDE.md                     # Reference guide for Antigravity config paths
├── TOOL_MAPPING.md                                 # Remote vs. local SecOps MCP tool mapping
└── LICENSE                                         # Apache 2.0 License
```

## License

Licensed under the [Apache License 2.0](LICENSE).
