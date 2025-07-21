#!/usr/bin/env python3
"""
BasicAuth module for handling Basic Authentication
"""
from api.v1.auth.auth import Auth
from flask import request
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class for basic HTTP authentication
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part from the Authorization header
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]
