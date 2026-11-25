# План реализации — TaskFlow

## Архитектура

- `taskmanager/` — конфигурация Django, подключение PostgreSQL/SQLite и Valkey/local cache через env.
- `tasks/` — модель, форма, представления, URL, admin, signals и тесты.
- `templates/`, `static/` — серверно-рендерируемый адаптивный интерфейс.
- `compose.yaml` — web + PostgreSQL 16 + Valkey 8 с healthcheck и volumes.
- `.opencode/` + `AGENTS.md` — локальные инструкции, собственный Skill и stdio MCP-интеграция для SDD.
- `docs/` — спецификация, план, задачи и ADR.

## Этапы (SDD)

1. **Discover:** определить проблему/пользователя/границы и зафиксировать критерии приёмки в `SPEC.md`.
2. **Design:** утвердить модель `Task`, UI-сценарии, cache key/invalidation, контейнерные сервисы и интеграцию OpenCode; записать решения в `DECISIONS.md`.
3. **Plan:** декомпозировать зависимости и критерии проверки в `TASKS.md`.
4. **Implement:** миграция и модель → CRUD/UI → фильтры/статистика → cache invalidation → инфраструктура и MCP.
5. **Verify:** Django system check, автоматические тесты, Compose build/up/healthcheck и ручная демонстрация.

## Риски и меры

- Valkey недоступен — в локальном режиме fallback на LocMemCache; контейнерный режим обязан использовать Valkey.
- PostgreSQL стартует медленнее web — `depends_on: condition: service_healthy`.
- Среда без Docker — тестировать через SQLite; контейнерный запуск пометить как непроверенный до Docker Desktop.
- MCP зависит от Python SDK — закрепить пакет в dev requirements, не выдавать MCP-инструментам операции записи.

## Definition of Done

Все критерии AC проверены; тесты и `manage.py check` проходят; миграции актуальны; README описывает запуск; Compose проверен на машине с Docker; MCP/Skill обнаруживаются OpenCode. Ограничения среды перечисляются явно.
