def test_players_are_public(client):
    resp = client.get("/api/players/")
    assert resp.status_code == 200


def test_favorites_require_auth(client):
    resp = client.get("/api/favorites/")
    assert resp.status_code == 401


def test_predictions_require_auth(client):
    resp = client.post("/api/predictions/", json={"player_id": 1})
    assert resp.status_code == 401
