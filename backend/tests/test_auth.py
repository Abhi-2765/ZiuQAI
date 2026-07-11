# backend/tests/test_auth.py
import pytest
from httpx import AsyncClient

async def test_auth_flow(client: AsyncClient):
    # 1. Register a new user
    register_payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "strongpassword123"
    }
    
    response = await client.post("/auth/register", json=register_payload)
    assert response.status_code == 200
    res_data = response.json()
    assert "user_code" in res_data
    user_code = res_data["user_code"]
    assert len(user_code) == 10
    
    # 2. Login
    login_payload = {
        "email": "testuser@example.com",
        "password": "strongpassword123"
    }
    response = await client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    assert "access_token" in response.cookies
    
    # Extract access token cookie
    token = response.cookies["access_token"]
    
    # 3. Get /me details
    client.cookies.set("access_token", token)
    response = await client.get("/auth/me")
    assert response.status_code == 200
    me_data = response.json()
    assert me_data["username"] == "testuser"
    assert me_data["email"] == "testuser@example.com"
    assert me_data["user_code"] == user_code
