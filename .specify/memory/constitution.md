<!-- SYNC IMPACT REPORT
Version change: 2.0.0 → 3.0.0
Modified principles: Added Phase III-specific principles for AI and MCP usage
Added sections: Phase III technology matrix with AI/MCP details, MCP-specific rules
Removed sections: Generic Phase III description
Templates requiring updates:
- ⚠ .specify/templates/plan-template.md - needs update for AI/MCP tools
- ⚠ .specify/templates/spec-template.md - needs update for AI/MCP specs
- ⚠ .specify/templates/tasks-template.md - needs update for AI/MCP tasks
Follow-up TODOs: Update templates to reflect new AI/MCP requirements
-->

# The Evolution of Todo - Project Constitution

## Core Principles

### I. Phase-Gated Development
All features and technologies must align with the current development phase. Phase I (in-memory console app) → Phase II (full-stack web app) → Phase III+ (advanced cloud/agents/AI). No technology or feature from a later phase may be introduced early without explicit approval and clear justification.

### II. Full-Stack Web Architecture
The application follows a modern full-stack architecture with a Python REST API backend, Neon Serverless PostgreSQL database, SQLModel for data management, and a Next.js frontend with React and TypeScript. All components must be designed to work cohesively within this architecture.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced. All new features must have comprehensive unit, integration, and end-to-end tests before merging.

### IV. Integration Testing
Focus areas requiring integration tests: API contract tests, Database interactions, Authentication flows, Frontend-backend communication, Shared schemas between services.

### V. Technology Compliance
All implementations must strictly adhere to the approved technology matrix. No unauthorized frameworks, libraries, or services may be introduced without explicit constitutional amendment. Technology choices must align with the current phase of development.

### VI. Authentication-First Design
Authentication and security must be considered from the initial design phase. Better Auth must be implemented for all user-facing features. All user data must be properly secured and access-controlled from the beginning of Phase II development.

### VII. AI and MCP Governance (Phase III+)
AI agents may ONLY interact with the system via MCP tools. MCP tools must not store in-memory state. Conversation context must be persisted and retrievable. No autonomous background agents. No multi-agent orchestration beyond documented scope. This principle ensures controlled and stateful AI interactions within the system.

### VIII. State Management (Phase III+)
All conversation and task state must be persisted in the database. MCP tools must be stateless and rely on database persistence. This ensures reliability, scalability, and proper state management for AI-driven interactions.


## Technology Matrix

### Phase I (Completed)
- Architecture: In-memory console application only
- Language: Python
- Interface: Command-line interface (CLI)
- Persistence: In-memory storage only
- Authentication: Not allowed
- External Dependencies: Python standard library (with optional rich/typer for CLI enhancement)

### Phase II (Current)
- Backend: Python REST API
- Database: Neon Serverless PostgreSQL
- ORM/Data layer: SQLModel or equivalent
- Frontend: Next.js (React, TypeScript)
- Authentication: Better Auth (signup/signin)
- Architecture: Full-stack web application
- Authentication: Allowed starting Phase II
- Web frontend: Allowed starting Phase II
- Neon PostgreSQL: Allowed starting Phase II

### Phase III (AI/MCP Enabled)
- AI Logic: OpenAI Agents SDK
- Conversational Interface: Stateless chat API
- Tooling: Model Context Protocol (MCP)
- MCP Server: Official MCP SDK
- Architecture: Agent-driven task management
- State Management: Persist conversation and task state in database
- MCP tools must be stateless and rely on database persistence
- Rules:
  - AI agents may ONLY interact with the system via MCP tools
  - MCP tools must not store in-memory state
  - Conversation context must be persisted and retrievable
  - Phase II authentication, frontend, and database remain unchanged
  - No autonomous background agents
  - No multi-agent orchestration beyond documented scope
- Authorization: This amendment authorizes AI and MCP usage starting Phase III only

## Development Workflow

### Feature Implementation Process
1. **Specification**: Every feature starts with a written specification in the specs/ folder
2. **Planning**: Architecture and technical approach must be documented in plan.md
3. **Task Breakdown**: Implementation tasks must be detailed in tasks.md
4. **Implementation**: Code following the approved specifications
5. **Testing**: All features must pass unit, integration, and acceptance tests
6. **Review**: Code review must verify constitutional compliance

### Code Quality Standards
- Clean, readable code over complex solutions
- Follow language-specific style guides (PEP 8 for Python, etc.)
- Comprehensive documentation for all modules, classes, and functions
- Proper error handling and graceful degradation
- Modular design with clear separation of concerns

## Governance

The constitution supersedes all other development practices. All pull requests and code reviews must verify constitutional compliance. Any deviation from these principles requires a formal constitutional amendment with proper documentation and approval.

Technology choices must be justified and aligned with the current development phase. Complexity must be justified with clear value propositions.

**Version**: 3.0.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2026-01-07
