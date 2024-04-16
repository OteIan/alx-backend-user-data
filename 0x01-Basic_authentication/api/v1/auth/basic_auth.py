#!/usr/bin/env python3
"""
Basic Auth module
"""
from api.v1.auth.auth import Auth
from typing import Tuple


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
        extract base64 authorization header
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        decode base64 authorization header
        """
        import base64

        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header.encode('utf-8')
                ).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):  # type: ignore
        """
        extract user credential
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":"))
