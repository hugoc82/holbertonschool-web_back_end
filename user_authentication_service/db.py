#!/usr/bin/env python3
"""
Module DB : gère la connexion à la base de données et les opérations utilisateurs.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    Classe DB : permet d'ajouter des utilisateurs dans la base SQLite.
    """

    def __init__(self) -> None:
        """Initialise une nouvelle instance de DB"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Retourne une session SQLAlchemy (créée une seule fois)."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Crée un nouvel utilisateur avec un email et un mot de passe haché.
        L'utilisateur est sauvegardé en base et retourné.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user
