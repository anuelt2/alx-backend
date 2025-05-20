#!/usr/bin/env python3
"""A basic Flask app with Babel config"""
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
app.url_map.strict_slashes = False


class Config:
    """Configuration for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

babel = Babel(app)


@app.route("/", methods=["GET"])
def index():
    """index route"""
    return render_template("1-index.html")


@babel.localeselector
def get_locale():
    """Determines the best match for supported languages"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
