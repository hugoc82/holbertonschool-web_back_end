#!/usr/bin/env python3
"""Flask app avec templates paramétrés et i18n.

Utilise Flask-Babel et un sélecteur de locale basé sur l'en-tête
Accept-Language pour afficher des chaînes traduites dans les templates.
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration de l'application i18n."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app: Flask = Flask(__name__)
app.config.from_object(Config)

babel: Babel = Babel()


def get_locale() -> str:
    """Retourne la meilleure langue correspondant à la requête."""
    return request.accept_languages.best_match(Config.LANGUAGES) or "en"


# Initialise Babel avec le sélecteur de locale personnalisé
babel.init_app(app, locale_selector=get_locale)


@app.route("/", strict_slashes=False)
def index() -> str:
    """Affiche la page d'accueil traduite."""
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
