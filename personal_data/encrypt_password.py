#!/usr/bin/env python3
"""Module for encrypting and validating passwords using bcrypt."""
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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against its hashed version.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain password to verify.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
