---
name: secops-environment
description: Google SecOps environment configuration parameters including Customer ID, Project ID, Region, and Server URL.
---

# Google SecOps Environment Context

When executing tools, custom commands, or skills that interact with Google SecOps (including detection engineering, alert triage, threat hunting, and case management), always use the following configured environment parameters:

*   **Google Cloud Project ID (`PROJECT_ID`)**: `${PROJECT_ID}`
*   **Chronicle Customer ID (`CUSTOMER_ID`)**: `${CUSTOMER_ID}`
*   **Chronicle Region (`REGION`)**: `${REGION}`
*   **Server URL (`SERVER_URL`)**: `${SERVER_URL}`

Whenever a SecOps MCP tool or workflow (such as `generate_threat_detection_opportunity`, `generate_synthetic_events`, `evaluate_rule_coverage`, `get_rule`, `generate_rules`, `create_rule`, `list_cases`, `udm_search`, etc.) requires a customer ID, project ID, region, or server URL parameter, always supply these exact configured values unless explicitly overridden by the user.
