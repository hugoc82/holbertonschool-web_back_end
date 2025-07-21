#!/usr/bin/env python3
"""Module for encrypting passwords using bcrypt."""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with automatic salt generation.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
