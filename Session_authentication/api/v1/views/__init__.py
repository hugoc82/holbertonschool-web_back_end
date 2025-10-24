"""__init__.py: module documentation.
Author: Ton Nom Ici
Date: 2025-10-24
"""
#!/usr/bin/env python3
""" Blueprint configuration for API views
"""
from flask import Blueprint
from models.user import User

# Create the Blueprint object
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import all the view modules
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *  # <-- ajout pour l'étape 7

# Load users from file
User.load_from_file()

