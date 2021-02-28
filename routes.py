from flask import jsonify
from flask import request
from app import create_app
from app import db
from werkzeug.datastructures import MultiDict
from forms import LoginForm
from forms import PlayerKickForm
from forms import PlayerBanForm
from flask import send_file
from models import User
from models import RCON
from models import PlayerBan
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_access_cookies
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
import subprocess

app = create_app()

RCON_PASSWORD = app.config["RCON_PASSWORD"]
SERVER_HOST = app.config["SERVER_HOST"]
SERVER_PORT = app.config["SERVER_PORT"]


@app.route("/")
def home():
    return send_file("public/index.html")


@app.route("/login", methods=["POST"])
def login():
    data = MultiDict(request.json)
    form = LoginForm(data)
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            access_token = create_access_token(identity=form.username.data)
            response = jsonify(authenticated=True, access_token=access_token)
            set_access_cookies(
                response, access_token, max_age=app.config["JWT_ACCESS_TOKEN_EXPIRES"]
            )
            user.update_last_seen()
            db.session.commit()
            return response, 200
        else:
            return jsonify(errors="Invalid username or password"), 401
    else:
        return jsonify(errors=form.errors), 401


@app.route("/logout")
@jwt_required()
def logout():
    response = jsonify({})
    unset_access_cookies(response)
    return response, 200


@app.route("/players")
@jwt_required()
def get_players():
    try:
        rcon = RCON(SERVER_HOST, SERVER_PORT, RCON_PASSWORD)
        players = rcon.status()
    except Exception as e:
        print(str(e))
        return jsonify({"error": "game server connection error"}), 500
    else:
        return jsonify({"players": players}), 200


@app.route("/playerkick", methods=["POST"])
@jwt_required()
def player_kick():
    form = PlayerKickForm()
    if form.validate_on_submit():
        try:
            rcon = RCON(SERVER_HOST, SERVER_PORT, RCON_PASSWORD)
            status = rcon.kick(form.data["num"])
        except Exception as e:
            print(str(e))
            return jsonify({"error": "error on player kick operation"}), 500
        else:
            return jsonify({"success": status}), 204
    return jsonify({"errors": form.errors}), 400


@app.route("/playerban", methods=["POST"])
@jwt_required()
def player_ban():
    form = PlayerBanForm()

    if form.validate_on_submit():
        player_name = form.name.data
        player_ip = form.address.data
        player_num = form.num.data

        ban_rec = PlayerBan.query.filter_by(ip=player_ip).first()

        if ban_rec:
            print("Player IP is already banned in database! Check IPtables conf")
            return jsonify({"error": "Ban command failed on system level"}), 500

        print(f"Will BAN IP: {player_ip} - Player: {player_name}")
        proc = subprocess.run(
            [
                "sudo",
                "iptables",
                "-I",
                "DOCKER-USER",
                "-s",
                player_ip,
                "-j",
                "DROP",
                "-m",
                "comment",
                "--comment",
                f"CoD2 Server: {player_name}",
            ],
            stdout=subprocess.DEVNULL,
        )

        if proc.returncode != 0:
            print("Ban command failed! - Improve logging here")
            return jsonify({"error": "Ban command failed on system level"}), 500

        rcon = RCON(SERVER_HOST, SERVER_PORT, RCON_PASSWORD)
        rcon.kick(player_num)

        player_ban = PlayerBan(
            name=player_name, ip=player_ip, banned_by=get_jwt_identity()
        )
        db.session.add(player_ban)
        db.session.commit()

        return jsonify(success=True), 200

    return jsonify({"errors": form.errors}), 400
