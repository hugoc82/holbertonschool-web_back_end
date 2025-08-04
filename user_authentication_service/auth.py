#!/usr/bin/env python3
"""
Module d'authentification :
contient les fonctions de hachage, de session et d'identification utilisateur.
"""

import bcrypt
import uuid
from typing import Optional
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash le mot de passe fourni avec un sel, en utilisant bcrypt.
    Retourne le hachage sous forme de bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Génère un UUID4 unique et le retourne sous forme de chaîne.
    Utilisé pour les identifiants de session ou de réinitialisation.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Classe Auth : gère les opérations d'authentification des utilisateurs.
    """

    def __init__(self) -> None:
        """
        Initialise une nouvelle instance d'Auth avec une base DB privée.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Enregistre un nouvel utilisateur avec email et mot de passe.
        Lève ValueError si l'utilisateur existe déjà.
        Retourne l'objet User sinon.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Vérifie si un email et un mot de passe sont valides.
        Retourne True si les identifiants sont corrects, False sinon.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except (NoResultFound, Exception):
            return False

    def create_session(self, email: str) -> Optional[str]:
        """
        Crée une session pour l'utilisateur donné si trouvé.
        Retourne l'identifiant de session (UUID), ou None si non trouvé.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Retourne l'utilisateur correspondant au session_id donné.
        Si aucun utilisateur ou session invalide, retourne None.
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
