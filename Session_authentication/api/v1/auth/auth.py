#!/usr/bin/env python3
"""
Authentication module
"""

from flask import request
from os import getenv


class Auth:
    """Template for all authentication systems"""

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """
        Determines if authentication is required.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        for excluded in excluded_paths:
            if excluded.endswith('*'):
                if path.startswith(excluded[:-1]):
                    return False
            elif path == excluded or path + '/' == excluded:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the value of the Authorization header.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None):
        """
        Placeholder for current_user, implemented in subclasses.
        """
        return None

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
