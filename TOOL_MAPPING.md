# Tool Mapping: Managed Remote MCP vs. Local Python MCP

This document maps tools between the managed remote Google SecOps MCP server (`secops` at `https://${REGION}-chronicle.googleapis.com/mcp`) and the optional local Python MCP server packages (`secops-mcp` and `secops-soar-mcp`).

## Registered Tool Selection Strategy

1. **Registered MCP Tools Only**: Always verify that Google SecOps MCP tools are present in the active session's registered tool list. If neither remote nor local SecOps MCP tools are registered, stop immediately and instruct the user to configure and enable the `google-secops` plugin rather than attempting raw HTTP or `gcloud` CLI calls.
2. **Prioritize Remote MCP Tools (`secops`)**: When connected to the managed remote Google SecOps MCP server, prefer the remote tool column below.
3. **Registered Local MCP Alternate**: Use the local Python MCP tool column only when a local SecOps MCP server is already registered in the session and the remote equivalent is absent.
4. **Adapt Multi-Step Workflows**: Natural language UDM queries require a two-step sequence on the remote server (`translate_udm_query` followed by `udm_search`), whereas the local server combines them in `search_security_events`.

| Category | Capability | Remote MCP Tool (`secops`) | Local MCP Tool (Python) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Case Management** | List Cases | `list_cases` | `list_cases` | |
| | Get Case Details | `get_case` | `get_case_full_details` | Remote `get_case` supports `expand='tasks,tags,products'`; combine with `list_case_alerts` / `list_case_comments` as needed. |
| | Comment on Case | `create_case_comment` | `post_case_comment` | |
| | Update Case | `update_case` | `change_case_priority` | Remote tool updates priority, status, and assignee. |
| | Close Case | `execute_bulk_close_case` | `close_case` | Concludes case with root cause and reason code. |
| **Case Alerts** | List Alerts for Case | `list_case_alerts` | `list_alerts_by_case` | |
| | List Events for Alert | `list_connector_events` | `list_events_by_alert` | |
| **Entities** | Search Entities | `search_entity` | `search_entity` | |
| | Get Involved Entities | `list_involved_entities` | `get_entities_by_alert_group_identifiers` | |
| **SIEM / UDM** | UDM Search (Structured) | `udm_search` | `search_udm` | |
| | UDM Search (Natural Language) | `translate_udm_query` -> `udm_search` | `search_security_events` | Remote requires two steps (translate then search). |
| | Entity Summary | `summarize_entity` | `lookup_entity` | Summarizes prevalence, first/last seen, and asset context. |
| | IoC Matching | `get_ioc_match` | `get_ioc_matches` | |
| **SIEM Alerts** | List SIEM Alerts | `list_security_alerts` | `list_security_alerts` | Lists detections/alerts directly from Google SecOps SIEM. |
| | Get SIEM Alert | `get_security_alert` | `get_security_alert` | |
| | Update SIEM Alert | `update_security_alert` | `update_security_alert` | |
| **Detection Engineering (YARA-L 2.0)** | List Rules | `list_rules` | `list_rules` | |
| | Get Rule | `get_rule` | `get_rule` | |
| | Create Rule | `create_rule` | `create_rule` | |
| | Validate Rule | `validate_rule` | `validate_rule` | Validates YARA-L 2.0 UDM detection rule compilation. |
| | Historical Rule Detections | `list_rule_detections` | `list_rule_detections` | |
| | Coverage Evaluation & TDOs | `generate_threat_detection_opportunity`, `generate_synthetic_events`, `evaluate_rule_coverage_long_running`, `get_operation`, `generate_rules` | *(Not available locally)* | Managed remote agentic detection engineering tools. |
