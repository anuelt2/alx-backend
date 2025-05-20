#!/usr/bin/env python3
"""A basic Flask app with Babel config"""
from datetime import datetime
import pytz
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime

app = Flask(__name__)
app.url_map.strict_slashes = False

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


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
    current_time = format_datetime(datetime.now(pytz.timezone(get_timezone())))
    return render_template("index.html", current_time=current_time)


@babel.localeselector
def get_locale():
    """Checks if an incoming request contains locale argument"""
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale

    user = g.get("user")
    if user:
        user_locale = user.get("locale")
        if user_locale in app.config["LANGUAGES"]:
            return user_locale

    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_user():
    """Returns a user dictionary or None"""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except TypeError:
        return None


@app.before_request
def before_request():
    """Uses `get_user` function to find a user"""
    user = get_user()
    if user:
        g.user = user


@babel.timezoneselector
def get_timezone():
    """Get timezone for incoming request"""
    url_tz = request.args.get("timezone")
    if url_tz:
        try:
            return pytz.timezone(url_tz).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    user = g.get("user")
    if user:
        user_tz = user.get("timezone")
        if user_tz:
            try:
                return pytz.timezone(user_tz).zone
            except pytz.exceptions.UnknownTimeZoneError:
                pass

    return app.config["BABEL_DEFAULT_TIMEZONE"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
