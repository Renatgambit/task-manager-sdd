# Project instructions

## Required workflow: SDD

This repository uses Specification-Driven Development. Before changing product behavior:

1. Read `docs/SPEC.md` and identify the relevant acceptance criteria.
2. Read `docs/PLAN.md` and `docs/TASKS.md`; keep the task status in sync with implementation.
3. If scope or behavior changes, update the spec first, then the plan and task list.
4. Implement the smallest change that satisfies the approved specification.
5. Add or update automated tests, run them, and record any unavailable checks accurately.
6. Summarize changed files, test results, and remaining work.

## Engineering rules

- Keep Django views thin; put domain behavior in models/forms/services.
- Do not commit secrets. Use `.env.example` as the template; `.env` is ignored.
- PostgreSQL is the production/container database. SQLite is allowed only for local tests/development.
- Valkey is a Redis-compatible cache. Invalidate dashboard cache whenever tasks change.
- Database schema changes require Django migrations.
- MCP tools in `.opencode/mcp_server/` must remain read-only and scoped to this repository.
- Never change unrelated files outside this project directory.
