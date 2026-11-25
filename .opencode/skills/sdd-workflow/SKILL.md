---
name: SDD Workflow
description: Use when planning or changing ExamPrep; keep specification, plan, tasks, implementation, and tests aligned using SDD.
---

# ExamPrep SDD workflow

1. Read `AGENTS.md`, `docs/SPEC.md`, `docs/PLAN.md`, and `docs/TASKS.md` before implementing a feature.
2. Restate which acceptance criteria the request affects. If behavior is not specified, ask before inventing product scope.
3. Update `docs/SPEC.md` first for a changed requirement, then update `docs/PLAN.md` and `docs/TASKS.md`.
4. Implement only the approved scope. Keep ORM changes accompanied by migrations; preserve PostgreSQL/Valkey behavior in Compose and SQLite/local cache fallbacks for tests.
5. Add regression tests for behavior and cache invalidation. Run `python manage.py check` and `python manage.py test` when dependencies are available.
6. Report completed criteria, commands and actual results, and any environment limitation. Never claim Docker/OpenCode integration passed unless it was exercised.

## Project invariants

- Card mutations use POST and Django CSRF protection.
- Search covers subject, topic, question, and answer; filters use declared model choices.
- Any StudyCard save or delete invalidates `examprep:dashboard:v1`.
- Only new and due review cards enter a study session; repeat-later moves the card to the next day.
- MCP tools are read-only and must resolve paths inside the project root.
