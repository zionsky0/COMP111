# Workspace & Tooling Operational Directives

## 1. MCP Tooling & Modal Permissions
- Do NOT repeatedly trigger blocking MCP tool calls (`notebooklm/ask_question`, etc.) if the client security sandbox raises confirmation dialogs or if headless browser actions fail.
- Always prefer direct workspace implementation, local execution, and file-based data ingestion first.

## 2. NotebookLM Web Ingestion Constraint
- The `notebooklm-mcp` headless browser automation encounters selector/overlay changes in Google NotebookLM's Angular UI when clicking `add_source`.
- When syncing content to NotebookLM, always export ready-to-ingest markdown source documents (e.g., `COMP111_NotebookLM_Source.md`) directly in the workspace alongside the direct share URL so the user can paste/upload with zero friction.

## 3. Autonomous Execution & Clean Workflows
- Keep autonomous progress smooth without stalling on external browser hooks.
- Validate all unit tests, scripts, and tutors locally before presenting solutions.
