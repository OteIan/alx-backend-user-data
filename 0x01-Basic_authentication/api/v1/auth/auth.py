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
        
        for i in excluded_paths:
            if i.endswith('*'):
                if path.startswith(i[:len(i) - 1]):
                    return False
        return False

    def authorization_header(self, request=None) -> None:
        """
        authorization_handler
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        current_user
        """
        return None
