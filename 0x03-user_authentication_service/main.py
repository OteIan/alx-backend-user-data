#!/usr/bin/env python3
"""
Integration test
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Tests Registering a user
    """
    url = f"{BASE_URL}/users"
    body = {'email': email, 'password': password}

    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    response = requests.post(url, data=body)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Tests loggin in with the wrong password
    """
    url = f"{BASE_URL}/sessions"
    body = {'email': email, 'password': password}

    response = requests.post(url, data=body)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Tests logging in with correct password
    """
    url = f"{BASE_URL}/sessions"
    body = {'email': email, 'password': password}

    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Tests requesting profile information while logged out
    """
    url = f"{BASE_URL}/profile"

    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Tests requesting profile information while logged in
    """
    url = f"{BASE_URL}/profile"
    session = {"session_id": session_id}

    response = requests.get(url, cookies=session)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Tests logging out
    """
    url = f"{BASE_URL}/sessions"
    session = {"session_id": session_id}

    response = requests.delete(url, cookies=session)
    assert response.status_code == 200
    assert response.url == f"{BASE_URL}/"


def reset_password_token(email: str) -> str:
    """
    Tests reset password roken
    """
    url = f"{BASE_URL}/reset_password"
    body = {"email": email}

    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()['email'] == email
    assert "reset_token" in response.json()
    token = response.json()['reset_token']

    response = requests.post(url, data={"email": "Fake@email"})
    assert response.status_code == 403

    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Tests updating a password
    """
    url = f"{BASE_URL}/reset_password"
    body = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }

    response = requests.put(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}

    body = {
        "email": "Fake@email",
        "reset_token": "Fake token",
        "new_password": "Fake password"
    }
    response = requests.put(url, data=body)
    assert response.status_code == 403


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
