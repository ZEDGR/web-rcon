from flask import Flask
from flask import jsonify
from flask import session
from flask_wtf.csrf import generate_csrf
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
from functools import wraps
import secrets
import os
from flask import send_file
from dotenv import load_dotenv
from dotenv import find_dotenv
import models

load_dotenv(find_dotenv())

app = Flask(__name__, static_folder="public/static", static_url_path="/public/static")
app.secret_key = os.getenv("FLASK_SECRET_KEY")

csrf = CSRFProtect(app)

RCON_PASSWORD = os.getenv("RCON_PASSWORD", None)
if not RCON_PASSWORD:
    raise Exception("Generic exception about missing HOST value")

SERVER_HOST = os.getenv("SERVER_HOST", None)

if not SERVER_HOST:
    raise Exception("Generic exception about missing HOST value")

SERVER_PORT = int(os.getenv("SERVER_PORT", 28960))


def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if "token" not in session and not session["token"]:
            return jsonify({}), 401
        return func(*args, **kwargs)

    return wrapped


class LoginForm(FlaskForm):
    rcon_password = TextField("Rcon Password", [DataRequired()])

    def validate_rcon_password(form, field):
        if field.data != RCON_PASSWORD:
            raise ValidationError("Invalid Rcon Password")


class PlayerKickForm(FlaskForm):
    player_num = TextField("Player Number", [DataRequired()])

    def validate_player_num(form, field):
        if not field.data.isnumeric():
            raise ValidationError("Invalid Player ID")


class PlayerBanForm(FlaskForm):
    player_ip = TextField("Player IP", [DataRequired()])


@app.after_request
def set_xsrf_cookie(response):
    response.set_cookie("XSRF-TOKEN", generate_csrf())
    return response


@app.route("/")
def home():
    return send_file("public/index.html")


@app.route("/login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session["token"] = secrets.token_urlsafe(16)
        return jsonify({"token": session["token"]}), 200
    else:
        return jsonify({"errors": form.errors}), 401


@login_required
@app.route("/players")
def get_players():
    try:
        rcon = models.RCON(SERVER_HOST, SERVER_PORT, RCON_PASSWORD)
        players = rcon.status()
    except Exception as e:
        print(str(e))
        return jsonify({"error": "game server connection error"}), 500
    else:
        return jsonify({"players": players}), 200


@login_required
@app.route("/playerkick", methods=["POST"])
def player_kick():
    form = PlayerKickForm()
    if form.validate_on_submit():
        try:
            rcon = models.RCON(SERVER_HOST, SERVER_PORT, RCON_PASSWORD)
            status = rcon.kick(form.data["player_num"])
        except Exception as e:
            print(str(e))
            return jsonify({"error": "error on player kick operation"}), 500
        else:
            return jsonify({"success": status}), 204
    return jsonify({"errors": form.errors}), 400


@login_required
@app.route("/playerban", methods=["POST"])
def player_ban(player_ip):
    # TODO create form for validation
    print(player_ip)
    return jsonify({}), 204
