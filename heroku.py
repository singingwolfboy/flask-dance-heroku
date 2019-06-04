import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.heroku import make_heroku_blueprint, heroku

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["HEROKU_OAUTH_CLIENT_ID"] = os.environ.get("HEROKU_OAUTH_CLIENT_ID")
app.config["HEROKU_OAUTH_CLIENT_SECRET"] = os.environ.get("HEROKU_OAUTH_CLIENT_SECRET")
heroku_bp = make_heroku_blueprint(scope="identity")
app.register_blueprint(heroku_bp, url_prefix="/login")


@app.route("/")
def index():
    if not heroku.authorized:
        return redirect(url_for("heroku.login"))
    resp = heroku.get("/account")
    assert resp.ok, resp.text
    return "You are {email} on Heroku".format(email=resp.json()["email"])
