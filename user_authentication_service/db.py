#!/usr/bin/env python3
"""
Module DB : gère la base de données des utilisateurs avec SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    Classe DB : permet de gérer les utilisateurs via SQLAlchemy.
    """

    def __init__(self) -> None:
        """Initialise une nouvelle instance de DB avec SQLite"""
        self._engine = create_engine("sqlite:///a.db", echo=False)  # <-- corrigé ici
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Retourne une session SQLAlchemy, une seule fois (memoization)."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Crée un utilisateur avec email et mot de passe haché.
        L'utilisateur est sauvegardé et retourné.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Recherche un utilisateur avec des filtres dynamiques.
        Lève NoResultFound si aucun résultat,
        Lève InvalidRequestError si filtre invalide.
        """
        if not kwargs:
            raise InvalidRequestError("Aucun filtre fourni.")

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("Aucun utilisateur trouvé.")
        except InvalidRequestError:
            raise InvalidRequestError("Requête invalide.")
        return user
