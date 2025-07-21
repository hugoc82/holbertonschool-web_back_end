#!/usr/bin/env python3
""" Main 6
"""
import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

# Crée un utilisateur test
user_email = "bob@hbtn.io"
user_clear_pwd = "H0lbertonSchool98!"
user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user: {} / {}".format(user.id, user.display_name()))
user.save()

# Génère le header Basic Auth encodé en base64
basic_clear = "{}:{}".format(user_email, user_clear_pwd)
basic_encoded = base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")
print("Basic Base64: {}".format(basic_encoded))
