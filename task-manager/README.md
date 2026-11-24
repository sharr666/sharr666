# Task Manager (مدیر کارها)

A small full-stack task manager: user registration/login with session cookies, and per-user
task CRUD with priority, due date and completion status. Bilingual-ready Persian (RTL) UI.

## Stack

- Backend: Python 3 standard library only (`http.server` + `sqlite3`) — no pip installs needed.
- Frontend: vanilla HTML/CSS/JS single page, served by the same server.
- Storage: SQLite file at `data/tasks.db` (override with `TASKMAN_DB` env var).
- Passwords: PBKDF2-HMAC-SHA256 (100k iterations, per-user salt). Sessions: random tokens in
  an `HttpOnly; SameSite=Lax` cookie, expiring after 7 days.

## Run

```bash
cd task-manager
python3 app.py
# open http://127.0.0.1:8000
```

Environment variables: `PORT` (default 8000), `HOST` (default 127.0.0.1), `TASKMAN_DB`.

## Test

```bash
cd task-manager
python3 -m unittest discover -s tests -v
```

## API

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/register` | `{username, password}` → creates account + session |
| POST | `/api/login` | `{username, password}` → session cookie |
| POST | `/api/logout` | invalidates session |
| GET | `/api/me` | current user |
| GET | `/api/tasks` | list current user's tasks |
| POST | `/api/tasks` | create task `{title, description?, priority?, due_date?}` |
| GET | `/api/tasks/<id>` | single task |
| PUT | `/api/tasks/<id>` | partial update (any of title/description/priority/due_date/completed) |
| DELETE | `/api/tasks/<id>` | delete task |

`priority` ∈ `low | normal | high`, `due_date` = `YYYY-MM-DD`. All `/api/*` routes except
register/login require the session cookie.
