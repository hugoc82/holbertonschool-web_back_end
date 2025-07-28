#!/usr/bin/env python3
"""
Session Authentication module
"""

from api.v1.auth.auth import Auth
from models.user import User
from os import getenv
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class that inherits from Auth.
    Manages Session IDs for authentication.
    """

    # Class attribute for storing session_id -> user_id mapping
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID for a given user_id.
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve a user ID based on a given session ID.
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """
        Returns the value of the cookie named by the env var SESSION_NAME.
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        if session_name is None:
            return None
        return request.cookies.get(session_name)

    def current_user(self, request=None):
        """
        Return a User instance based on the session cookie.
        """
        if request is None:
            return None

        # Get session_id from cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        # Get user_id linked to this session_id
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Retrieve User instance from database
        return User.get(user_id)
