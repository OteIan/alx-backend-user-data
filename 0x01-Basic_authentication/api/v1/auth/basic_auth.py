#!/usr/bin/env python3
"""
Basic Auth module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class
    """
    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        extract_base64_authorization_header
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
