#!/usr/bin/env python3
""" Authentication module
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for a given path
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        # Normalise le path pour toujours finir avec /
        if not path.endswith('/'):
            path += '/'

        for excluded in excluded_paths:
            if excluded == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the Authorization header from the request
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return current user (not implemented)
        """
        return None
