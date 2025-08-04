#!/usr/bin/env python3
"""
Module d'authentification :
gestion des utilisateurs, sessions, mots de passe et réinitialisations.
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

    def get_user_from_session_id(self,
                                 session_id: str) -> Optional[User]:
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

    def destroy_session(self, user_id: int) -> None:
        """
        Supprime la session d'un utilisateur en mettant session_id à None.
        Ne retourne rien.
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Génère un token de réinitialisation de mot de passe pour un email donné.
        Lève ValueError si l'utilisateur n'existe pas.
        Retourne le token UUID généré.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Met à jour le mot de passe utilisateur via un token de réinitialisation.
        Lève ValueError si le token est invalide.
        """
        if not reset_token or not password:
            raise ValueError

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed,
                             reset_token=None)
