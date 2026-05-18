def test_update_task_partial(client):
    # status만 변경 — 나머지 필드 유지
    created = client.post("/api/tasks", json={
        "title": "원래 제목",
        "description": "원래 설명",
    }).json()
    res = client.put(f"/api/tasks/{created['id']}", json={"status": "in_progress"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "in_progress"
    assert data["title"] == "원래 제목"      # 유지
    assert data["description"] == "원래 설명"  # 유지


def test_update_task_updated_at_changes(client):
    created = client.post("/api/tasks", json={"title": "태스크"}).json()
    updated = client.put(
        f"/api/tasks/{created['id']}", json={"title": "수정된 제목"}
    ).json()
    assert updated["title"] == "수정된 제목"


def test_update_task_not_found(client):
    # 404 — 존재하지 않는 id
    res = client.put("/api/tasks/99999", json={"status": "done"})
    assert res.status_code == 404


def test_update_task_invalid_status(client):
    # 422 — 허용되지 않는 status 값
    created = client.post("/api/tasks", json={"title": "태스크"}).json()
    res = client.put(f"/api/tasks/{created['id']}", json={"status": "invalid"})
    assert res.status_code == 422
