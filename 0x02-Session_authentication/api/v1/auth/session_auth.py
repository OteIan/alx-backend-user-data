#!/usr/bin/python3
"""
Session Auth Module
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session Auth class
    """
    def __init__(self) -> None:
        super().__init__()
