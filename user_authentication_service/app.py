#!/usr/bin/env python3
"""
Application Flask pour l'enregistrement des utilisateurs.
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome() -> str:
    """
    Route de base : retourne un message de bienvenue.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> tuple:
    """
    Route POST /users : enregistre un nouvel utilisateur.
    Retourne un JSON de confirmation ou une erreur si déjà inscrit.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": user.email,
            "message": "user created"
        }), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
