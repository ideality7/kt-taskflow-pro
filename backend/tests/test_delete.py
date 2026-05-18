def test_delete_task_success(client):
    created = client.post("/api/tasks", json={"title": "삭제할 태스크"}).json()
    res = client.delete(f"/api/tasks/{created['id']}")
    assert res.status_code == 204
    assert res.content == b""  # 응답 바디 없음


def test_delete_task_then_get_returns_404(client):
    created = client.post("/api/tasks", json={"title": "삭제 후 조회"}).json()
    client.delete(f"/api/tasks/{created['id']}")
    res = client.get(f"/api/tasks/{created['id']}")
    assert res.status_code == 404


def test_delete_task_not_found(client):
    # 404 — 존재하지 않는 id
    res = client.delete("/api/tasks/99999")
    assert res.status_code == 404
