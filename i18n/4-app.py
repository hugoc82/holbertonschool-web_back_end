#!/usr/bin/env python3
"""Flask app with URL-forced locale (i18n step 4).

Adds support for forcing the locale via a `locale` query parameter,
falling back to the client's Accept-Language header when absent/invalid.
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
    """Return forced locale via ?locale=... or best match from headers."""
    forced = request.args.get("locale")
    if forced in Config.LANGUAGES:
        return forced
    return request.accept_languages.best_match(Config.LANGUAGES) or "en"


# Initialise Babel avec le sélecteur de langue personnalisé
babel.init_app(app, locale_selector=get_locale)


@app.route("/", strict_slashes=False)
def index() -> str:
    """Render the translated home page."""
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
