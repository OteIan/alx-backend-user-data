#!/usr/bin/env python3
"""
Session authentication module
"""
from models.user_session import UserSession
from flask import request
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class
    """
    def create_session(self, user_id: str = None) -> str:
        """
        Create session
        """
        session_id = super().create_session(user_id)

        if isinstance(session_id, str):
            kwargs = {
                'user_id': user_id,
                'session_id': session_id
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        User id for session id
        """
        try:
            session = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(session) <= 0:
            return None
        current_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        total_time = session[0].created_at + time_span

        if current_time > total_time:
            return None
        return session_id[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroy session
        """
        session_id = self.session_cookie(request)
        session = UserSession.search({'session_id': session_id})

        if not session and len(session) <= 0:
            return False

        session[0].remove()
        return True
