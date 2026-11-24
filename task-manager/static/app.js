const $ = (id) => document.getElementById(id);

const PRIORITY_FA = { low: "کم", normal: "متوسط", high: "زیاد" };

let authMode = "login";

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.error || "خطای ناشناخته");
    err.status = res.status;
    err.fields = data.fields || {};
    throw err;
  }
  return data;
}

function show(view) {
  $("auth-view").classList.toggle("hidden", view !== "auth");
  $("tasks-view").classList.toggle("hidden", view !== "tasks");
}

function setAuthMode(mode) {
  authMode = mode;
  $("tab-login").classList.toggle("active", mode === "login");
  $("tab-register").classList.toggle("active", mode === "register");
  $("auth-submit").textContent = mode === "login" ? "ورود" : "ثبت‌نام";
  $("auth-error").textContent = "";
}

async function refreshMe() {
  try {
    const data = await api("/api/me");
    $("me").textContent = data.user.username;
    show("tasks");
    await loadTasks();
  } catch {
    show("auth");
  }
}

async function loadTasks() {
  try {
    const data = await api("/api/tasks");
    renderTasks(data.tasks);
    $("tasks-error").textContent = "";
  } catch (err) {
    if (err.status === 401) {
      show("auth");
    } else {
      $("tasks-error").textContent = err.message;
    }
  }
}

function renderTasks(tasks) {
  const list = $("task-list");
  list.innerHTML = "";
  $("empty-msg").classList.toggle("hidden", tasks.length > 0);
  for (const task of tasks) {
    list.appendChild(taskElement(task));
  }
}

function taskElement(task) {
  const li = document.createElement("li");
  li.className = "task card prio-" + task.priority + (task.completed ? " completed" : "");
  li.dataset.id = task.id;

  const check = document.createElement("input");
  check.type = "checkbox";
  check.checked = task.completed;
  check.title = "انجام شد";
  check.addEventListener("change", async () => {
    try {
      await api("/api/tasks/" + task.id, {
        method: "PUT",
        body: JSON.stringify({ completed: check.checked }),
      });
      await loadTasks();
    } catch (err) {
      check.checked = !check.checked;
      $("tasks-error").textContent = err.message;
    }
  });

  const body = document.createElement("div");
  body.className = "task-body";

  const title = document.createElement("span");
  title.className = "task-title";
  title.textContent = task.title;

  const meta = document.createElement("div");
  meta.className = "task-meta";
  const prio = document.createElement("span");
  prio.className = "badge prio-" + task.priority;
  prio.textContent = "اولویت " + (PRIORITY_FA[task.priority] || task.priority);
  meta.appendChild(prio);
  if (task.due_date) {
    const due = document.createElement("span");
    due.className = "badge due";
    due.textContent = "سررسید: " + task.due_date;
    meta.appendChild(due);
  }

  body.appendChild(title);
  if (task.description) {
    const desc = document.createElement("p");
    desc.className = "task-desc";
    desc.textContent = task.description;
    body.appendChild(desc);
  }
  body.appendChild(meta);

  const actions = document.createElement("div");
  actions.className = "task-actions";

  const editBtn = document.createElement("button");
  editBtn.type = "button";
  editBtn.textContent = "ویرایش";
  editBtn.addEventListener("click", () => startEdit(li, task));

  const delBtn = document.createElement("button");
  delBtn.type = "button";
  delBtn.textContent = "حذف";
  delBtn.className = "danger";
  delBtn.addEventListener("click", async () => {
    if (!confirm("این کار حذف شود؟")) return;
    try {
      await api("/api/tasks/" + task.id, { method: "DELETE" });
      await loadTasks();
    } catch (err) {
      $("tasks-error").textContent = err.message;
    }
  });

  actions.appendChild(editBtn);
  actions.appendChild(delBtn);

  li.appendChild(check);
  li.appendChild(body);
  li.appendChild(actions);
  return li;
}

function startEdit(li, task) {
  if (li.classList.contains("editing")) return;
  li.classList.add("editing");
  const body = li.querySelector(".task-body");
  const actions = li.querySelector(".task-actions");
  body.innerHTML = "";
  actions.innerHTML = "";

  const titleInput = document.createElement("input");
  titleInput.value = task.title;
  titleInput.maxLength = 200;

  const descInput = document.createElement("textarea");
  descInput.value = task.description || "";
  descInput.rows = 2;

  const prioSelect = document.createElement("select");
  for (const p of Object.keys(PRIORITY_FA)) {
    const opt = document.createElement("option");
    opt.value = p;
    opt.textContent = PRIORITY_FA[p];
    if (p === task.priority) opt.selected = true;
    prioSelect.appendChild(opt);
  }

  const dueInput = document.createElement("input");
  dueInput.type = "date";
  dueInput.value = task.due_date || "";

  const saveBtn = document.createElement("button");
  saveBtn.type = "button";
  saveBtn.textContent = "ذخیره";
  saveBtn.addEventListener("click", async () => {
    try {
      await api("/api/tasks/" + task.id, {
        method: "PUT",
        body: JSON.stringify({
          title: titleInput.value,
          description: descInput.value,
          priority: prioSelect.value,
          due_date: dueInput.value || null,
        }),
      });
      await loadTasks();
    } catch (err) {
      $("tasks-error").textContent = err.message;
    }
  });

  const cancelBtn = document.createElement("button");
  cancelBtn.type = "button";
  cancelBtn.textContent = "لغو";
  cancelBtn.addEventListener("click", () => loadTasks());

  body.appendChild(titleInput);
  body.appendChild(descInput);
  body.appendChild(prioSelect);
  body.appendChild(dueInput);
  actions.appendChild(saveBtn);
  actions.appendChild(cancelBtn);
}

$("tab-login").addEventListener("click", () => setAuthMode("login"));
$("tab-register").addEventListener("click", () => setAuthMode("register"));

$("auth-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("auth-error").textContent = "";
  const payload = { username: $("username").value, password: $("password").value };
  try {
    await api(authMode === "login" ? "/api/login" : "/api/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    $("password").value = "";
    await refreshMe();
  } catch (err) {
    $("auth-error").textContent = err.message;
  }
});

$("logout-btn").addEventListener("click", async () => {
  await api("/api/logout", { method: "POST", body: "{}" });
  show("auth");
});

$("task-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("tasks-error").textContent = "";
  try {
    await api("/api/tasks", {
      method: "POST",
      body: JSON.stringify({
        title: $("task-title").value,
        description: $("task-desc").value,
        priority: $("task-priority").value,
        due_date: $("task-due").value || null,
      }),
    });
    $("task-title").value = "";
    $("task-desc").value = "";
    $("task-due").value = "";
    $("task-title").focus();
    await loadTasks();
  } catch (err) {
    $("tasks-error").textContent = err.message;
  }
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/static/sw.js").catch(() => {});
  });
}

refreshMe();
