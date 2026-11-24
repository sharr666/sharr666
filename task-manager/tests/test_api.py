import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.cookiejar import CookieJar

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app


class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        db_path = os.path.join(cls.tmp.name, "test.db")
        cls.server = app.create_server(port=0, host="127.0.0.1", db_path=db_path)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.tmp.cleanup()

    def request(self, method, path, body=None, jar=None):
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        handlers = []
        if jar is not None:
            handlers.append(urllib.request.HTTPCookieProcessor(jar))
        opener = urllib.request.build_opener(*handlers)
        try:
            with opener.open(req) as res:
                return res.status, json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read().decode("utf-8"))

    def test_full_flow(self):
        jar_a = CookieJar()
        jar_b = CookieJar()

        status, body = self.request("POST", "/api/register", {"username": "alice", "password": "secret1"}, jar_a)
        self.assertEqual(status, 201)
        self.assertEqual(body["user"]["username"], "alice")

        status, body = self.request("POST", "/api/register", {"username": "alice", "password": "secret1"}, CookieJar())
        self.assertEqual(status, 409)

        status, body = self.request("POST", "/api/register", {"username": "x", "password": "secret1"}, CookieJar())
        self.assertEqual(status, 400)

        status, body = self.request("POST", "/api/login", {"username": "alice", "password": "wrong-pass"}, CookieJar())
        self.assertEqual(status, 401)

        status, body = self.request("GET", "/api/me", jar=jar_a)
        self.assertEqual(status, 200)
        self.assertEqual(body["user"]["username"], "alice")

        status, body = self.request("GET", "/api/tasks", jar=CookieJar())
        self.assertEqual(status, 401)

        status, body = self.request("POST", "/api/tasks",
                                    {"title": "Buy milk", "priority": "high", "due_date": "2026-12-01"}, jar_a)
        self.assertEqual(status, 201)
        task1 = body["task"]
        self.assertEqual(task1["title"], "Buy milk")
        self.assertFalse(task1["completed"])

        status, body = self.request("POST", "/api/tasks", {"title": ""}, jar_a)
        self.assertEqual(status, 400)

        status, body = self.request("POST", "/api/tasks", {"title": "Read book", "priority": "urgent"}, jar_a)
        self.assertEqual(status, 400)

        status, body = self.request("POST", "/api/tasks", {"title": "Read book"}, jar_a)
        self.assertEqual(status, 201)
        task2 = body["task"]
        self.assertEqual(task2["priority"], "normal")

        status, body = self.request("GET", "/api/tasks", jar=jar_a)
        self.assertEqual(status, 200)
        self.assertEqual(len(body["tasks"]), 2)
        self.assertEqual(body["tasks"][0]["id"], task1["id"])

        status, body = self.request("PUT", f"/api/tasks/{task2['id']}",
                                    {"completed": True, "priority": "low"}, jar_a)
        self.assertEqual(status, 200)
        self.assertTrue(body["task"]["completed"])
        self.assertEqual(body["task"]["priority"], "low")

        status, body = self.request("PUT", f"/api/tasks/{task2['id']}", {"due_date": "not-a-date"}, jar_a)
        self.assertEqual(status, 400)

        status, body = self.request("GET", "/api/tasks", jar=jar_b)
        self.assertEqual(status, 401)

        status, body = self.request("POST", "/api/register", {"username": "bob", "password": "secret2"}, jar_b)
        self.assertEqual(status, 201)
        status, body = self.request("GET", "/api/tasks", jar=jar_b)
        self.assertEqual(body["tasks"], [])

        status, body = self.request("GET", f"/api/tasks/{task1['id']}", jar=jar_b)
        self.assertEqual(status, 404)

        status, body = self.request("DELETE", f"/api/tasks/{task1['id']}", jar=jar_b)
        self.assertEqual(status, 404)

        status, body = self.request("DELETE", f"/api/tasks/{task1['id']}", jar=jar_a)
        self.assertEqual(status, 200)

        status, body = self.request("GET", "/api/tasks", jar=jar_a)
        self.assertEqual(len(body["tasks"]), 1)

        status, body = self.request("POST", "/api/logout", {}, jar_a)
        self.assertEqual(status, 200)
        status, body = self.request("GET", "/api/me", jar=jar_a)
        self.assertEqual(status, 401)

        status, body = self.request("POST", "/api/login", {"username": "alice", "password": "secret1"}, jar_a)
        self.assertEqual(status, 200)
        status, body = self.request("GET", "/api/me", jar=jar_a)
        self.assertEqual(status, 200)

    def test_static_index(self):
        req = urllib.request.Request(self.base + "/")
        with urllib.request.build_opener().open(req) as res:
            self.assertEqual(res.status, 200)
            self.assertIn(b"rtl", res.read())

    def test_static_traversal_blocked(self):
        status, body = self.request("GET", "/static/../app.py")
        self.assertEqual(status, 404)

    def test_pwa_assets_served(self):
        import urllib.request as ur
        for path in ("/static/manifest.webmanifest", "/static/sw.js", "/static/icon.svg"):
            with ur.build_opener().open(self.base + path) as res:
                self.assertEqual(res.status, 200, path)
        with ur.build_opener().open(self.base + "/static/manifest.webmanifest") as res:
            manifest = json.loads(res.read().decode("utf-8"))
        self.assertEqual(manifest["start_url"], "/")
        self.assertEqual(manifest["display"], "standalone")
        self.assertEqual(manifest["dir"], "rtl")


if __name__ == "__main__":
    unittest.main()
