#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Auth class
    """
    def __init__(self) -> None:
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> None:
        """
        authorization_handler
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        current_user
        """
        return None
