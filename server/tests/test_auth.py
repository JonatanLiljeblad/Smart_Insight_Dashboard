def test_register(client):
    resp = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "secret123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "full_name": "User", "password": "pass"}
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 400


def test_login(client):
    client.post("/api/auth/register", json={
        "email": "login@example.com",
        "full_name": "Login User",
        "password": "secret123",
    })
    resp = client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "secret123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "email": "u@example.com",
        "full_name": "User",
        "password": "right",
    })
    resp = client.post("/api/auth/login", json={
        "email": "u@example.com",
        "password": "wrong",
    })
    assert resp.status_code == 401


def test_me(client):
    client.post("/api/auth/register", json={
        "email": "me@example.com",
        "full_name": "Me User",
        "password": "secret123",
    })
    login_resp = client.post("/api/auth/login", json={
        "email": "me@example.com",
        "password": "secret123",
    })
    token = login_resp.json()["access_token"]
    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@example.com"


def test_me_unauthorized(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401
