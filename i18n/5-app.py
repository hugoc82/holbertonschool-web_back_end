#!/usr/bin/env python3
"""Flask app with mocked login and i18n (step 5).

- Force locale via ?locale=...
- Mock user login via ?login_as=<user_id>
- Expose g.user avant chaque requête
- Affiche un message différent selon la connexion
"""

from typing import Optional, Dict, Any

from flask import Flask, g, render_template, request
from flask_babel import Babel


class Config:
    """Configuration de l'application i18n."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Mock de "table" utilisateurs
users: Dict[int, Dict[str, Any]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app: Flask = Flask(__name__)
app.config.from_object(Config)

babel: Babel = Babel()


def get_locale() -> str:
    """Retourne la locale forcée (?locale=...) ou le meilleur match."""
    forced = request.args.get("locale")
    if forced in Config.LANGUAGES:
        return forced
    return request.accept_languages.best_match(Config.LANGUAGES) or "en"


# Initialise Babel avec sélecteur de langue personnalisé
babel.init_app(app, locale_selector=get_locale)


def get_user() -> Optional[Dict[str, Any]]:
    """Récupère l'utilisateur depuis ?login_as, sinon None."""
    login_as = request.args.get("login_as")
    if not login_as:
        return None
    try:
        uid = int(login_as)
    except (TypeError, ValueError):
        return None
    return users.get(uid)


@app.before_request
def before_request() -> None:
    """Définit g.user avant chaque requête si un user est trouvé."""
    g.user = get_user()


@app.route("/", strict_slashes=False)
def index() -> str:
    """Affiche la page d'accueil traduite avec message de login."""
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
