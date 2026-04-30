def test_list_players_returns_public_catalog(client, sample_player):
    resp = client.get("/api/players/")
    assert resp.status_code == 200
    assert resp.json()[0]["name"] == sample_player.name


def test_get_player_returns_player_detail(client, sample_player):
    resp = client.get(f"/api/players/{sample_player.id}")
    assert resp.status_code == 200
    assert resp.json()["external_id"] == sample_player.external_id


def test_get_player_stats_returns_ordered_history(client, sample_player, sample_player_stats):
    resp = client.get(f"/api/players/{sample_player.id}/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert [row["event_date"] for row in data] == [
        "2025-01-15",
        "2025-02-05",
        "2025-02-26",
    ]


def test_get_unknown_player_returns_404(client):
    resp = client.get("/api/players/999")
    assert resp.status_code == 404
