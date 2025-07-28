#!/usr/bin/env python3
"""
Session Authentication module
"""

from api.v1.auth.auth import Auth
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

        Args:
            user_id (str): The user ID to associate with a new session.

        Returns:
            str: The session ID created, or None if input is invalid.
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        # Generate a new session ID
        session_id = str(uuid.uuid4())

        # Store mapping of session_id -> user_id
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve a user ID based on a given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID,
                 or None if not found or invalid.
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)
