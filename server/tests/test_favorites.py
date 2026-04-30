def test_add_and_list_favorites(client, auth_headers, sample_player):
    create_resp = client.post(
        "/api/favorites/",
        json={"player_id": sample_player.id},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201

    list_resp = client.get("/api/favorites/", headers=auth_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
    assert list_resp.json()[0]["player_id"] == sample_player.id


def test_add_favorite_rejects_duplicates(client, auth_headers, sample_player):
    payload = {"player_id": sample_player.id}
    client.post("/api/favorites/", json=payload, headers=auth_headers)

    resp = client.post("/api/favorites/", json=payload, headers=auth_headers)
    assert resp.status_code == 409


def test_add_favorite_requires_existing_player(client, auth_headers):
    resp = client.post(
        "/api/favorites/",
        json={"player_id": 999},
        headers=auth_headers,
    )
    assert resp.status_code == 404


def test_remove_favorite_deletes_owned_record(client, auth_headers, sample_player):
    create_resp = client.post(
        "/api/favorites/",
        json={"player_id": sample_player.id},
        headers=auth_headers,
    )
    favorite_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/api/favorites/{favorite_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    list_resp = client.get("/api/favorites/", headers=auth_headers)
    assert list_resp.json() == []
