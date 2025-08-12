#!/usr/bin/env python3
"""Flask app using user locale preference (step 6).

Priorité de sélection de langue :
1) Paramètre d'URL ?locale
2) Préférence de l'utilisateur (si connecté)
3) En-tête Accept-Language de la requête
4) Locale par défaut ("en")
"""

from typing import Optional, Dict, Any

from flask import Flask, g, render_template, request
from flask_babel import Babel


class Config:
    """Configuration i18n pour l'application."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Mock "table" d'utilisateurs
users: Dict[int, Dict[str, Any]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app: Flask = Flask(__name__)
app.config.from_object(Config)

babel: Babel = Babel()


def get_user() -> Optional[Dict[str, Any]]:
    """Retourne l'utilisateur depuis ?login_as, sinon None."""
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
    """Expose l'utilisateur courant dans g.user avant chaque requête."""
    g.user = get_user()


def get_locale() -> str:
    """Détermine la locale selon la priorité demandée."""
    # 1) Query param
    forced = request.args.get("locale")
    if forced in Config.LANGUAGES:
        return forced

    # 2) User preference
    user = getattr(g, "user", None)
    if user:
        user_locale = user.get("locale")
        if user_locale in Config.LANGUAGES:
            return user_locale

    # 3) Accept-Language header
    best = request.accept_languages.best_match(Config.LANGUAGES)
    if best:
        return best

    # 4) Default
    return Config.BABEL_DEFAULT_LOCALE


# Initialise Babel avec notre sélecteur de locale
babel.init_app(app, locale_selector=get_locale)


@app.route("/", strict_slashes=False)
def index() -> str:
    """Affiche la page d'accueil traduite avec message de login."""
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
