#!/usr/bin/env python3
"""
Basic Auth module
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


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

        split_decoded = decoded_base64_authorization_header.split(":")
        user_email = split_decoded[0]
        user_pwd = ":".join(split_decoded[1:])
        return (user_email, user_pwd)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):  # type: ignore
        """
        user object from credentials
        """
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """
        current user
        """
        try:
            auth_header = self.authorization_header(request)
            b64_auth_header = self.extract_base64_authorization_header(
                auth_header)
            decoded_b64_auth_header = self.decode_base64_authorization_header(
                b64_auth_header)
            user_email, user_pwd = self.extract_user_credentials(
                decoded_b64_auth_header)

            return self.user_object_from_credentials(user_email, user_pwd)
        except Exception:
            return None
