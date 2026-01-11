---
id: 1
title: "Amend Phase III Constitution AI MCP"
stage: constitution
date_iso: "2026-01-07"
surface: "agent"
model: "Qwen"
feature: "none"
branch: "main"
user: "Dell"
command: "/sp.constitution"
labels:
  - "constitution"
  - "phase-iii"
  - "ai"
  - "mcp"
  - "governance"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
  - "history/prompts/constitution/1-amend-phase-iii-constitution-ai-mcp.constitution.prompt.md"
tests_yaml: []
---

# Amendment to Project Constitution for Phase III AI and MCP Capabilities

## User Input

```
/sp.constitution Amend the global constitution to enable Phase III capabilities as follows:

Phase III:
- AI Logic: OpenAI Agents SDK
- Conversational Interface: Stateless chat API
- Tooling: Model Context Protocol (MCP)
- MCP Server: Official MCP SDK
- Architecture: Agent-driven task management
- State Management: Persist conversation and task state in database
- MCP tools must be stateless and rely on database persistence

Rules:
- AI agents may ONLY interact with the system via MCP tools
- MCP tools must not store in-memory state
- Conversation context must be persisted and retrievable
- Phase II authentication, frontend, and database remain unchanged
- No autonomous background agents
- No multi-agent orchestration beyond documented scope

This amendment authorizes AI and MCP usage starting Phase III only.
```

## Response Summary

Updated the project constitution to version 3.0.0 to enable Phase III capabilities with specific AI and MCP governance rules. Added two new core principles (VII and VIII) and updated the Phase III technology matrix with detailed specifications for AI/MCP usage.

## Outcome

The constitution was successfully updated with:
- New version 3.0.0 reflecting major governance changes
- Principle VII: AI and MCP Governance (Phase III+)
- Principle VIII: State Management (Phase III+)
- Detailed Phase III technology matrix with AI/MCP specifics
- Rules for MCP tool usage and state management
- Sync Impact Report documenting all changes

Files requiring manual updates were identified in the Sync Impact Report.