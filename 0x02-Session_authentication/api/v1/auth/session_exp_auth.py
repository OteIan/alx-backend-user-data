#!/usr/bin/env python3
""" SessionExpAuth module
"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class
    """
    def __init__(self) -> None:
        """Initializer
        """
        super.__init__()
        if os.getenv('SESSION_DURATION'):
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        else:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        SessionExpAuth.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        if session_id in self.user_id_by_session_id:
            if self.session_duration <= 0:
                return session_id
            session_dict = self.user_id_by_session_id[session_id]
            if 'created_at' not in session_dict:
                return None
            created_at = session_dict['created_at']
            if (datetime.now() - created_at).seconds > self.session_duration:
                return None
            return session_dict['user_id']
