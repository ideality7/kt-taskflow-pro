def test_get_task_success(client):
    created = client.post("/api/tasks", json={
        "title": "단건 조회 태스크",
        "description": "설명 포함",
    }).json()
    res = client.get(f"/api/tasks/{created['id']}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == created["id"]
    assert data["description"] == "설명 포함"  # 단건은 description 포함


def test_get_task_not_found(client):
    # 404 — 존재하지 않는 id
    res = client.get("/api/tasks/99999")
    assert res.status_code == 404
