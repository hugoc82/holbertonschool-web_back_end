#!/usr/bin/env python3
"""
Module d'authentification : contient les fonctions liées au hash des mots de passe.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash le mot de passe fourni avec un sel, en utilisant bcrypt.
    Retourne le hachage sous forme de bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
