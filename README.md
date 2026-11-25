# TaskFlow — трекер задач (ЛР, вариант №5)

Учебный веб-трекер задач на Django. Работа организована по SDD: **спецификация → план → задачи → реализация**. Для контейнерного запуска используются PostgreSQL и Valkey; OpenCode подключается к локальному MCP-серверу проекта и обнаруживает Skill из `.opencode/skills/`.

## Возможности

- список задач с поиском и фильтром по статусу;
- создание, редактирование, удаление и перевод задачи в следующий статус;
- приоритет, описание и срок выполнения;
- карточки статистики на главной странице, кэшируемые в Valkey;
- автоматическая очистка кэша после изменения задачи;
- Django admin для демонстрации модели;
- MCP-инструменты для чтения SDD-статуса и перечня документов.

## Запуск в Docker (рекомендуется)

Требуются Docker Desktop с включённым Linux containers и Docker Compose v2.

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Откройте <http://localhost:8000>. Остановка: `Ctrl+C`; удалить контейнеры: `docker compose down`. Данные PostgreSQL хранятся в именованном volume и не удаляются командой `down`.

Создать администратора:

```powershell
docker compose exec web python manage.py createsuperuser
```

Админка: <http://localhost:8000/admin/>.

## Локальная разработка без Docker

Нужен Python 3.11+; Django использует SQLite, если `DB_HOST` не задан. В локальном режиме `DEBUG` включён, чтобы dev-сервер отдавал CSS из папки `static/`; не используйте встроенный `runserver` как production-сервер.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```

Откройте <http://127.0.0.1:8000>. Для локального режима без PostgreSQL/Valkey приложение работает на SQLite и локальном кэше; полноценная конфигурация варианта №5 — Docker Compose.

## Проверки

```powershell
python manage.py check
python manage.py test
```

## OpenCode, Skill и MCP

Откройте в OpenCode именно папку `task-manager-sdd`. Проектная конфигурация `.opencode/opencode.json` поднимает read-only MCP-сервер `taskflow-docs` через Python из `.venv`. Создайте окружение и установите dev-зависимости:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Проверьте сервер через `/mcps` или `opencode mcp list`; инструменты должны показывать SDD-статус и доступные документы. Skill `sdd-workflow` находится в `.opencode/skills/sdd-workflow/SKILL.md`, глобальная инструкция — в `AGENTS.md`.

## SDD-артефакты

- `docs/SPEC.md` — проблема, пользователи, требования и критерии приёмки;
- `docs/PLAN.md` — архитектура и план по этапам;
- `docs/TASKS.md` — чек-лист работ и тестирования;
- `docs/DECISIONS.md` — зафиксированные проектные решения.

## Стек

Python 3.11+, Django 5.2, PostgreSQL 16, Valkey 8, Docker Compose, MCP Python SDK.
