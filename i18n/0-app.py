#!/usr/bin/env python3
"""Basic Flask app for the i18n project.

This module exposes a single index route that renders a simple
welcome page.
"""

from flask import Flask, render_template

app: Flask = Flask(__name__)


@app.route("/", strict_slashes=False)
def index() -> str:
    """Render the home page with a static title and header."""
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
