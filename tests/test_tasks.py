from datetime import datetime
from uuid import UUID


def test_create_task(client):
    r = client.post("/tasks", json={"title": "A", "description": "d", "done": False})
    assert r.status_code == 201
    body = r.json()

    assert UUID(body["id"])
    assert body["title"] == "A"
    assert body["description"] == "d"
    assert body["done"] is False

    assert "created_at" in body
    assert "updated_at" in body


def test_list_tasks_filter_and_pagination(client):
    t1 = client.post("/tasks", json={"title": "t1", "done": False}).json()
    t2 = client.post("/tasks", json={"title": "t2", "done": True}).json()
    t3 = client.post("/tasks", json={"title": "t3", "done": False}).json()

    r = client.get("/tasks")
    assert r.status_code == 200
    assert len(r.json()) == 3

    r = client.get("/tasks", params={"done": "false"})
    assert r.status_code == 200
    titles = [x["title"] for x in r.json()]
    assert set(titles) == {"t1", "t3"}

    r = client.get("/tasks", params={"limit": 1, "offset": 1})
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_get_task_success_and_404(client):
    created = client.post("/tasks", json={"title": "hello"}).json()
    task_id = created["id"]

    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200
    assert r.json()["id"] == task_id

    r = client.get("/tasks/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


def test_patch_task_updates_updated_at(client):
    created = client.post("/tasks", json={"title": "x", "done": False}).json()
    task_id = created["id"]
    created_at = datetime.fromisoformat(created["created_at"])
    updated_at_1 = datetime.fromisoformat(created["updated_at"])

    r = client.patch(f"/tasks/{task_id}", json={"done": True, "title": "y"})
    assert r.status_code == 200
    body = r.json()
    assert body["done"] is True
    assert body["title"] == "y"

    updated_at_2 = datetime.fromisoformat(body["updated_at"])
    assert updated_at_2 >= updated_at_1
    assert datetime.fromisoformat(body["created_at"]) == created_at

    r = client.patch("/tasks/00000000-0000-0000-0000-000000000000", json={"done": True})
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "delme"}).json()
    task_id = created["id"]

    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 204
    assert r.text == ""

    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 404

    r = client.delete("/tasks/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"
