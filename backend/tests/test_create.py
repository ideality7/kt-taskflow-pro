def test_create_task_success(client):
    res = client.post("/api/tasks", json={"title": "테스트 태스크"})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "테스트 태스크"
    assert data["status"] == "todo"
    assert data["description"] is None
    assert "id" in data


def test_create_task_with_all_fields(client):
    res = client.post("/api/tasks", json={
        "title": "전체 필드 태스크",
        "description": "상세 설명",
        "status": "in_progress",
        "due_at": "2026-12-31T09:00:00Z",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["description"] == "상세 설명"
    assert data["status"] == "in_progress"
    assert data["due_at"] is not None


def test_create_task_missing_title(client):
    # 422 — title 누락
    res = client.post("/api/tasks", json={"status": "todo"})
    assert res.status_code == 422


def test_create_task_empty_title(client):
    # 422 — title 빈 문자열
    res = client.post("/api/tasks", json={"title": ""})
    assert res.status_code == 422


def test_create_task_title_too_long(client):
    # 422 — title 200자 초과
    res = client.post("/api/tasks", json={"title": "a" * 201})
    assert res.status_code == 422


def test_create_task_invalid_status(client):
    # 422 — 허용되지 않는 status 값
    res = client.post("/api/tasks", json={"title": "태스크", "status": "invalid"})
    assert res.status_code == 422
