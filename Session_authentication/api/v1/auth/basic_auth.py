#!/usr/bin/env python3
"""
BasicAuth module for handling Basic Authentication
"""
from api.v1.auth.auth import Auth
from flask import request
from typing import TypeVar, Tuple
import base64
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class for basic HTTP authentication
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts Base64 part from Authorization header"""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes Base64 authorization string"""
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extracts email and password from decoded Base64 string"""
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns User instance from email and password"""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves User instance from request"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        b64_part = self.extract_base64_authorization_header(auth_header)
        if b64_part is None:
            return None

        decoded = self.decode_base64_authorization_header(b64_part)
        if decoded is None:
            return None

        email, pwd = self.extract_user_credentials(decoded)
        if email is None or pwd is None:
            return None

        return self.user_object_from_credentials(email, pwd)
