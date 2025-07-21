#!/usr/bin/env python3
"""
Basic authentication module for the API.
Handles base64 decoding of the Authorization header.
"""
from api.v1.auth.auth import Auth
from flask import request
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ BasicAuth class for basic authentication """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        Args:
            authorization_header: The full authorization header
        Returns:
            The Base64 part of the header or None
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]
