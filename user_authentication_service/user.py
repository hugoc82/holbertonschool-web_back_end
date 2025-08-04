#!/usr/bin/env python3
"""
Ce module définit un modèle SQLAlchemy pour un utilisateur,
représentant la table users dans la base de données.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    Modèle SQLAlchemy pour la table users. Ce modèle définit
    la structure des enregistrements utilisateurs utilisés pour
    l'authentification et la gestion de session.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)
