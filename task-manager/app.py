import hashlib
import json
import os
import re
import secrets
import sqlite3
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DEFAULT_DB = os.path.join(BASE_DIR, "data", "tasks.db")

SESSION_TTL = timedelta(days=7)
SESSION_COOKIE_MAX_AGE = int(SESSION_TTL.total_seconds())
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,32}$")
PRIORITIES = ("low", "normal", "high")
MAX_BODY = 1_000_000

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".webmanifest": "application/manifest+json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
}

_write_lock = threading.Lock()


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def get_db(db_path):
    conn = sqlite3.connect(db_path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    return conn


def init_db(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_db(db_path)
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                pass_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                expires_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high')),
                due_date TEXT,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 100_000)
    return f"{salt}${digest.hex()}"


def verify_password(password, stored):
    try:
        salt, digest = stored.split("$", 1)
    except ValueError:
        return False
    candidate = hash_password(password, salt).split("$", 1)[1]
    return secrets.compare_digest(candidate, digest)


def session_cookie(token, max_age=SESSION_COOKIE_MAX_AGE):
    return f"session={token}; Path=/; HttpOnly; SameSite=Lax; Max-Age={max_age}"


def validate_task_payload(data, partial):
    fields = {}
    errors = {}
    if not partial or "title" in data:
        title = str(data.get("title", "")).strip()
        if not title or len(title) > 200:
            errors["title"] = "title must be 1-200 characters"
        else:
            fields["title"] = title
    if "description" in data:
        fields["description"] = str(data.get("description") or "")[:2000]
    if "priority" in data:
        priority = data.get("priority")
        if priority not in PRIORITIES:
            errors["priority"] = "priority must be one of: low, normal, high"
        else:
            fields["priority"] = priority
    if "due_date" in data:
        due = data.get("due_date")
        if due in (None, ""):
            fields["due_date"] = None
        else:
            try:
                datetime.strptime(str(due), "%Y-%m-%d")
                fields["due_date"] = str(due)
            except ValueError:
                errors["due_date"] = "due_date must be YYYY-MM-DD"
    if "completed" in data:
        fields["completed"] = 1 if data.get("completed") else 0
    return fields, errors


def task_to_dict(row):
    data = dict(row)
    data.pop("user_id", None)
    data["completed"] = bool(data["completed"])
    return data


class Handler(BaseHTTPRequestHandler):
    server_version = "TaskManager/1.0"
    db_path = DEFAULT_DB

    def log_message(self, *args):
        pass

    def send_json(self, status, payload, extra_headers=None):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for key, value in (extra_headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return None
        if length <= 0:
            return {}
        if length > MAX_BODY:
            return None
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None
        return data if isinstance(data, dict) else None

    def session_token(self):
        cookie = self.headers.get("Cookie", "")
        for part in cookie.split(";"):
            key, _, value = part.strip().partition("=")
            if key == "session" and value:
                return value
        return None

    def current_user(self):
        token = self.session_token()
        if not token:
            return None
        conn = get_db(self.db_path)
        try:
            row = conn.execute(
                "SELECT u.id, u.username FROM sessions s JOIN users u ON u.id = s.user_id "
                "WHERE s.token = ? AND s.expires_at > ?",
                (token, utcnow()),
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def require_user(self):
        user = self.current_user()
        if user is None:
            self.send_json(401, {"error": "authentication required"})
        return user

    def serve_static(self, path):
        if path in ("/", "/index.html"):
            rel = "index.html"
        elif path.startswith("/static/"):
            rel = path[len("/static/"):]
        else:
            self.send_json(404, {"error": "not found"})
            return
        full = os.path.normpath(os.path.join(STATIC_DIR, rel))
        if not full.startswith(STATIC_DIR + os.sep) or not os.path.isfile(full):
            self.send_json(404, {"error": "not found"})
            return
        ext = os.path.splitext(full)[1].lower()
        with open(full, "rb") as handle:
            body = handle.read()
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPES.get(ext, "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def handle_register(self, data):
        username = str(data.get("username", "")).strip()
        password = str(data.get("password", ""))
        errors = {}
        if not USERNAME_RE.match(username):
            errors["username"] = "username must be 3-32 chars of letters, digits or underscore"
        if len(password) < 6 or len(password) > 128:
            errors["password"] = "password must be 6-128 characters"
        if errors:
            self.send_json(400, {"error": "invalid input", "fields": errors})
            return
        conn = get_db(self.db_path)
        try:
            with _write_lock:
                exists = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
                if exists:
                    self.send_json(409, {"error": "username already taken"})
                    return
                cursor = conn.execute(
                    "INSERT INTO users (username, pass_hash, created_at) VALUES (?, ?, ?)",
                    (username, hash_password(password), utcnow()),
                )
                user_id = cursor.lastrowid
                token = secrets.token_urlsafe(32)
                expires = (datetime.now(timezone.utc) + SESSION_TTL).isoformat()
                conn.execute(
                    "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
                    (token, user_id, expires),
                )
                conn.commit()
            self.send_json(201, {"user": {"id": user_id, "username": username}},
                           {"Set-Cookie": session_cookie(token)})
        finally:
            conn.close()

    def handle_login(self, data):
        username = str(data.get("username", "")).strip()
        password = str(data.get("password", ""))
        conn = get_db(self.db_path)
        try:
            row = conn.execute("SELECT id, username, pass_hash FROM users WHERE username = ?", (username,)).fetchone()
            if row is None or not verify_password(password, row["pass_hash"]):
                self.send_json(401, {"error": "invalid username or password"})
                return
            with _write_lock:
                token = secrets.token_urlsafe(32)
                expires = (datetime.now(timezone.utc) + SESSION_TTL).isoformat()
                conn.execute(
                    "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
                    (token, row["id"], expires),
                )
                conn.commit()
            self.send_json(200, {"user": {"id": row["id"], "username": row["username"]}},
                           {"Set-Cookie": session_cookie(token)})
        finally:
            conn.close()

    def handle_logout(self):
        token = self.session_token()
        if token:
            conn = get_db(self.db_path)
            try:
                with _write_lock:
                    conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
                    conn.commit()
            finally:
                conn.close()
        self.send_json(200, {"ok": True}, {"Set-Cookie": session_cookie("", max_age=0)})

    def handle_list_tasks(self, user):
        conn = get_db(self.db_path)
        try:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE user_id = ? ORDER BY completed ASC, "
                "CASE priority WHEN 'high' THEN 0 WHEN 'normal' THEN 1 ELSE 2 END, created_at DESC",
                (user["id"],),
            ).fetchall()
            self.send_json(200, {"tasks": [task_to_dict(r) for r in rows]})
        finally:
            conn.close()

    def handle_create_task(self, user, data):
        fields, errors = validate_task_payload(data, partial=False)
        if errors:
            self.send_json(400, {"error": "invalid input", "fields": errors})
            return
        now = utcnow()
        conn = get_db(self.db_path)
        try:
            with _write_lock:
                cursor = conn.execute(
                    "INSERT INTO tasks (user_id, title, description, priority, due_date, completed, created_at, updated_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        user["id"],
                        fields["title"],
                        fields.get("description", ""),
                        fields.get("priority", "normal"),
                        fields.get("due_date"),
                        fields.get("completed", 0),
                        now,
                        now,
                    ),
                )
                conn.commit()
                row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
            self.send_json(201, {"task": task_to_dict(row)})
        finally:
            conn.close()

    def get_task(self, user, task_id):
        conn = get_db(self.db_path)
        try:
            row = conn.execute(
                "SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user["id"])
            ).fetchone()
            return conn, row
        except Exception:
            conn.close()
            raise

    def handle_update_task(self, user, task_id, data):
        fields, errors = validate_task_payload(data, partial=True)
        if errors:
            self.send_json(400, {"error": "invalid input", "fields": errors})
            return
        conn, row = self.get_task(user, task_id)
        try:
            if row is None:
                self.send_json(404, {"error": "task not found"})
                return
            if not fields:
                self.send_json(400, {"error": "no fields to update"})
                return
            fields["updated_at"] = utcnow()
            assignments = ", ".join(f"{key} = ?" for key in fields)
            with _write_lock:
                conn.execute(f"UPDATE tasks SET {assignments} WHERE id = ? AND user_id = ?",
                             (*fields.values(), task_id, user["id"]))
                conn.commit()
                updated = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            self.send_json(200, {"task": task_to_dict(updated)})
        finally:
            conn.close()

    def handle_delete_task(self, user, task_id):
        conn, row = self.get_task(user, task_id)
        try:
            if row is None:
                self.send_json(404, {"error": "task not found"})
                return
            with _write_lock:
                conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user["id"]))
                conn.commit()
            self.send_json(200, {"ok": True})
        finally:
            conn.close()

    def route_api(self, method, path, data):
        if method == "POST" and path == "/api/register":
            self.handle_register(data)
            return
        if method == "POST" and path == "/api/login":
            self.handle_login(data)
            return
        if method == "POST" and path == "/api/logout":
            self.handle_logout()
            return
        if method == "GET" and path == "/api/me":
            user = self.require_user()
            if user:
                self.send_json(200, {"user": user})
            return
        if path == "/api/tasks":
            user = self.require_user()
            if not user:
                return
            if method == "GET":
                self.handle_list_tasks(user)
            elif method == "POST":
                self.handle_create_task(user, data)
            else:
                self.send_json(405, {"error": "method not allowed"})
            return
        if path.startswith("/api/tasks/"):
            user = self.require_user()
            if not user:
                return
            try:
                task_id = int(path[len("/api/tasks/"):])
            except ValueError:
                self.send_json(404, {"error": "task not found"})
                return
            if method == "PUT":
                self.handle_update_task(user, task_id, data)
            elif method == "DELETE":
                self.handle_delete_task(user, task_id)
            elif method == "GET":
                conn, row = self.get_task(user, task_id)
                try:
                    if row is None:
                        self.send_json(404, {"error": "task not found"})
                    else:
                        self.send_json(200, {"task": task_to_dict(row)})
                finally:
                    conn.close()
            else:
                self.send_json(405, {"error": "method not allowed"})
            return
        self.send_json(404, {"error": "not found"})

    def dispatch(self, method):
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            data = self.read_json()
            if data is None:
                self.send_json(400, {"error": "invalid JSON body"})
                return
            self.route_api(method, path, data)
        elif method == "GET":
            self.serve_static(path)
        else:
            self.send_json(405, {"error": "method not allowed"})

    def do_GET(self):
        self.dispatch("GET")

    def do_POST(self):
        self.dispatch("POST")

    def do_PUT(self):
        self.dispatch("PUT")

    def do_DELETE(self):
        self.dispatch("DELETE")


def create_server(port=8000, host="127.0.0.1", db_path=DEFAULT_DB):
    init_db(db_path)
    Handler.db_path = db_path
    return ThreadingHTTPServer((host, port), Handler)


def main():
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "127.0.0.1")
    db_path = os.environ.get("TASKMAN_DB", DEFAULT_DB)
    server = create_server(port=port, host=host, db_path=db_path)
    print(f"Task Manager running at http://{server.server_address[0]}:{server.server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
