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

## Mobile (PWA)

The UI is responsive (single-column layout and 44px touch targets under 520px) and the app is a
Progressive Web App: `manifest.webmanifest` + SVG icon + service worker (`sw.js`) cache the shell
so it loads fast and works offline; API calls fall back to a 503 JSON error when offline.

To use it on a phone on the same Wi-Fi, run on your own machine:

```bash
HOST=0.0.0.0 PORT=8000 python3 app.py
# then open http://<your-computer-ip>:8000 on the phone
```

In Chrome/Edge on Android use "Add to Home screen"; on iOS Safari use Share → "Add to Home Screen".
Note: installing the PWA requires HTTPS or localhost; over plain LAN HTTP the app still works in
the browser, it just cannot be installed to the home screen. The server binds to `127.0.0.1` by
default — only set `HOST=0.0.0.0` on a network you trust.

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
