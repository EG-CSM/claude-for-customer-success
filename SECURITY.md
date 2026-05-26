# Security Policy

## Reporting a Vulnerability

**Do not open a public GitHub Issue to report a security vulnerability.**

If you discover a vulnerability in this repository — including prompt injection risks in skill content, insecure MCP configuration patterns, hook intercept bypasses, or credential exposure in managed agent cookbooks — report it privately:

**Email**: [security@successhacker.co](mailto:security@successhacker.co)
**Subject line**: [Security] claude-for-customer-success — <brief description>

Include:

- A description of the vulnerability and its potential impact
- The file(s) and line(s) involved
- Steps to reproduce or a proof-of-concept if applicable

We will acknowledge receipt within 5 business days and work with you on a coordinated disclosure timeline.

**Scope note**. Most security-relevant behavior in this suite is governed by Claude's model-level safety systems, Anthropic's usage policies, and the access permissions you configure on your MCP connectors. The skills and plugins in this repo do not execute code or make API calls directly — they are prompts and configuration files. The primary security surface is data access: what connectors you authorize, what data those connectors can reach, and who has access to the Claude session that invokes the skills. Review the Disclaimer for data handling guidance.
