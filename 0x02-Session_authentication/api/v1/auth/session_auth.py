#!/usr/bin/python3
"""
Session Auth Module
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Session Auth class
    """
    user_id_by_session_id = {}

    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """
        create session
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        user id for session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)
