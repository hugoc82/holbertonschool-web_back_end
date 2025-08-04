#!/usr/bin/env python3
"""
Application Flask basique pour l'authentification.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome() -> str:
    """
    Route de base : retourne un message de bienvenue en JSON.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
