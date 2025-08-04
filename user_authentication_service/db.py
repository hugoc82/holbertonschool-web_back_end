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
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Retourne une session SQLAlchemy, créée une seule fois (mémoïsée).
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Crée un utilisateur avec email et mot de passe haché.
        Enregistre et retourne l'objet User.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Recherche un utilisateur via des filtres dynamiques.
        Lève NoResultFound si aucun résultat,
        Lève InvalidRequestError si les champs sont invalides.
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

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Met à jour les attributs d'un utilisateur identifié par user_id.
        Lève ValueError si une clé ne correspond à aucun attribut de User.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                msg = f"'{key}' n'est pas un attribut valide de User"
                raise ValueError(msg)
            setattr(user, key, value)

        self._session.commit()
