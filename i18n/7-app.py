#!/usr/bin/env python3
"""Flask app with user locale and timezone selection (step 7).

Priorité de la locale :
1) Paramètre d'URL ?locale
2) Préférence utilisateur (si connecté)
3) En-tête Accept-Language
4) Valeur par défaut ("en")

Priorité du fuseau horaire :
1) Paramètre d'URL ?timezone
2) Préférence utilisateur (si connecté)
3) Valeur par défaut ("UTC")

Les timezones sont validées via pytz.timezone, sinon fallback sur UTC.
"""

from typing import Optional, Dict, Any

from flask import Flask, g, render_template, request
from flask_babel import Babel, format_datetime
import pytz
from pytz.exceptions import UnknownTimeZoneError


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


def get_locale() -> str:
    """Détermine la locale selon la priorité spécifiée."""
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


def _validate_timezone(tz: Optional[str]) -> Optional[str]:
    """Valide un identifiant de timezone avec pytz, sinon None."""
    if not tz:
        return None
    try:
        pytz.timezone(tz)
    except UnknownTimeZoneError:
        return None
    return tz


def get_timezone() -> str:
    """Retourne le fuseau horaire en respectant la priorité et la validation."""
    # 1) Query param
    tz = _validate_timezone(request.args.get("timezone"))
    if tz:
        return tz

    # 2) User preference
    user = getattr(g, "user", None)
    if user:
        tz = _validate_timezone(user.get("timezone"))
        if tz:
            return tz

    # 3) Default
    return Config.BABEL_DEFAULT_TIMEZONE


# Initialise Babel avec nos sélecteurs
babel.init_app(
    app,
    locale_selector=get_locale,
    timezone_selector=get_timezone
)


@app.before_request
def before_request() -> None:
    """Expose l'utilisateur et infos debug avant chaque requête."""
    g.user = get_user()
    g.debug_locale = get_locale()
    g.debug_timezone = get_timezone()


@app.route("/", strict_slashes=False)
def index() -> str:
    """Affiche la page d'accueil traduite avec message de login."""
    return render_template("7-index.html", now=format_datetime())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
