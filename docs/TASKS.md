# Реестр задач (SDD)

Статусы: `[x]` реализовано в исходниках; `[ ]` требует проверки/действия в среде с Docker/OpenCode.

## Спецификация и дизайн

- [x] Зафиксировать персону, проблему, сценарии и scope — `SPEC.md`.
- [x] Определить критерии приёмки AC-1…AC-8.
- [x] Зафиксировать архитектурные решения — `DECISIONS.md`.

## Приложение

- [x] Создать Django-проект и конфигурацию SQLite/PostgreSQL.
- [x] Добавить модель Task, choices и начальную миграцию.
- [x] Реализовать список, детали, создание, редактирование, удаление, переход статуса.
- [x] Добавить поиск, фильтр, статистику и адаптивные шаблоны.
- [x] Подключить Valkey cache и сигнал инвалидации.
- [x] Добавить admin и тесты сценариев.
- [x] Установить Python-зависимости и выполнить `manage.py check` / тесты на SQLite: 8 тестов прошли.

## Инфраструктура и инструменты OpenCode

- [x] Добавить Dockerfile и Compose для Django + PostgreSQL + Valkey, healthchecks и volumes.
- [x] Добавить `.env.example` и исключить `.env` из Git.
- [x] Добавить SDD инструкции в `AGENTS.md` и Skill `sdd-workflow`.
- [x] Добавить read-only MCP server с инструментами чтения SDD; MCP SDK handshake и оба инструмента проверены.
- [ ] Запустить Docker Compose, проверить healthchecks и сценарии браузера.
- [ ] Открыть проект в OpenCode, проверить `/mcps` и загрузить Skill (CLI OpenCode не установлен/не найден).
- [ ] Оформить Git-репозиторий/коммиты после установки Git и согласования авторства коммитов.

## Команды проверки

```powershell
python manage.py check
python manage.py test
docker compose config
docker compose up --build
```
