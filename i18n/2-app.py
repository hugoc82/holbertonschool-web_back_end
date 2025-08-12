#!/usr/bin/env python3
"""Flask app with Babel locale selection from the request.

This module configures Flask-Babel and uses a custom locale selector
that picks the best match from the client's Accept-Language header.
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Application configuration for i18n."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app: Flask = Flask(__name__)
app.config.from_object(Config)

# Crée l'instance Babel au niveau du module
babel: Babel = Babel()


def get_locale() -> str:
    """Return the best-matched locale based on the request headers."""
    return request.accept_languages.best_match(Config.LANGUAGES) or "en"


# Initialise Babel avec l'app et le sélecteur de langue personnalisé
babel.init_app(app, locale_selector=get_locale)


@app.route("/", strict_slashes=False)
def index() -> str:
    """Render the home page."""
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
