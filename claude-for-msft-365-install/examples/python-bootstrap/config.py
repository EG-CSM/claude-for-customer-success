"""
Edit this file to configure your bootstrap server. app.py should not need changes.
"""
import base64
import os

# ─── Config ──────────────────────────────────────────────────────────
TENANT_ID = os.environ["TENANT_ID"]                         # your Entra tenant
AUDIENCE  = "c2995f31-11e7-4882-b7a7-ef9def0a0266"          # Claude in Office add-in app ID
ISSUER    = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
JWKS_URL  = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
HOST      = os.getenv("HOST", "127.0.0.1")
PORT      = int(os.getenv("PORT", "8080"))

# Local-dev override: point at a self-issued JWKS instead of Entra.
# Signature verification still runs. Refuses to start on non-loopback.
DEV_JWKS_PATH = os.getenv("DEV_JWKS_PATH")
if DEV_JWKS_PATH and HOST != "127.0.0.1":
    raise SystemExit("DEV_JWKS_PATH may only be used when HOST=127.0.0.1")

# ─── Catalog: every skill / MCP server you might hand out ────────────
def b64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()

SKILLS = {
    "account-health-summary": {
        "description": "Summarize account health signals and risk indicators",
        "url": "https://your-bucket.s3.amazonaws.com/skills/account-health-summary.zip?X-Amz-Signature=...",
    },
    "renewal-risk-brief": {
        "description": "Generate a renewal risk brief from CRM and health data",
        "content": b64("# Renewal risk brief\n\nAnalyze the account for renewal risk signals..."),
    },
    "qbr-prep": {
        "description": "Prepare a QBR agenda and talking points from account data",
        "url": "https://your-bucket.s3.amazonaws.com/skills/qbr-prep.zip?X-Amz-Signature=...",
    },
}

MCP_SERVERS = {
    "salesforce-crm": {"url": "https://mcp.salesforce.com/sse", "label": "Salesforce CRM"},
    "gainsight-cs": {
        "url": "https://internal.example.com/mcp/gainsight",
        "label": "Gainsight",
        "headers": {"Authorization": "Bearer {{gateway_token}}"},
    },
    "hubspot-crm": {"url": "https://mcp.hubspot.com/sse", "label": "HubSpot CRM"},
}

# ─── RBAC: first matching rule wins ──────────────────────────────────
# `when` conditions (all must match):
#   group — value from the Entra token's `groups` claim
#   user  — Entra user `oid`
#   app   — Office host: "word" | "excel" | "powerpoint"
# In production, group/user values are GUIDs — replace the names below
# with real Object IDs from Entra admin center.
RULES = [
    {"when": {"app": "excel", "group": "enterprise-csm"},
     "skills": ["account-health-summary", "qbr-prep"], "mcp_servers": ["salesforce-crm", "gainsight-cs"]},

    {"when": {"group": "renewals"},
     "skills": ["renewal-risk-brief", "account-health-summary"], "mcp_servers": ["salesforce-crm"]},

    {"when": {"group": "cs-ops"},
     "skills": ["account-health-summary"], "mcp_servers": ["gainsight-cs", "salesforce-crm"]},

    {"when": {}, "skills": ["account-health-summary"], "mcp_servers": []},  # default
]
