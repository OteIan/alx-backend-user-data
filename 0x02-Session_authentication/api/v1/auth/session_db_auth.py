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
        if user_id is None:
            return None
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
        if session_id is None:
            return None
        
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})

        if not user_session:
            return None
        
        user_session = user_session[0]

        start_time = user_session.created_at
        time_delta = timedelta(seconds=self.session_duration)

        if (start_time + time_delta) < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroy session
        """
        session_id = self.session_cookie(request)
        if session_id is None or not self.user_id_for_session_id(session_id):
            return False
        
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False

        user_session = user_session[0]
        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        
        return True
