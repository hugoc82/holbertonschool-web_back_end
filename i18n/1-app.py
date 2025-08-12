#!/usr/bin/env python3
"""Flask app with basic Babel setup for the i18n project.

This module configures Flask-Babel with a default locale and timezone,
and exposes a single index route rendering a simple template.
"""

from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Application configuration for i18n."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app: Flask = Flask(__name__)
app.config.from_object(Config)

# Expose a module-level Babel instance as required
babel: Babel = Babel(app)


@app.route("/", strict_slashes=False)
def index() -> str:
    """Render the home page."""
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
