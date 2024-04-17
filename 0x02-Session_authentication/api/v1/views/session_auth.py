#!/usr/bin/env python3
""" Module for Session views
"""
import os
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    JSON representaion of a User object
    """
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        user_list = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    if not user_list[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user_list[0].id)
    response = jsonify(user_list[0].to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response
