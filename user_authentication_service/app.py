#!/usr/bin/env python3
"""
Application Flask pour l'authentification des utilisateurs.
"""

from flask import Flask, jsonify, request, abort, make_response
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
    Retourne un message de confirmation ou d'erreur.
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


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """
    Route POST /sessions : connecte un utilisateur si les
    identifiants sont valides. Retourne un message JSON et
    définit un cookie session_id. Sinon, renvoie une 401.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(401)

    response = make_response(jsonify({
        "email": email,
        "message": "logged in"
    }))
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
