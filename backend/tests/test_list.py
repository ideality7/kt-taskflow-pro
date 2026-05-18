def test_list_tasks_empty(client):
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert res.json() == []


def test_list_tasks_returns_items(client):
    client.post("/api/tasks", json={"title": "태스크 1"})
    client.post("/api/tasks", json={"title": "태스크 2", "status": "done"})
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_list_tasks_excludes_description(client):
    # 목록 응답에 description 없어야 함
    client.post("/api/tasks", json={"title": "태스크", "description": "설명"})
    res = client.get("/api/tasks")
    assert "description" not in res.json()[0]


def test_list_tasks_filter_by_status(client):
    client.post("/api/tasks", json={"title": "할 일", "status": "todo"})
    client.post("/api/tasks", json={"title": "진행 중", "status": "in_progress"})
    res = client.get("/api/tasks?status=todo")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["status"] == "todo"
