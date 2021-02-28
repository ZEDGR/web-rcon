from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from dotenv import find_dotenv
import os
import click
from getpass import getpass
from datetime import timedelta

load_dotenv(find_dotenv())

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(
        __name__, static_folder="public/static", static_url_path="/public/static"
    )
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    if app.env == "production":
        app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        hours=int(os.getenv("FLASK_JWT_EXPIRATION_IN_HOURS"))
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("FLASK_DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    RCON_PASSWORD = os.getenv("RCON_PASSWORD", None)
    if not RCON_PASSWORD:
        raise Exception("Generic exception about missing HOST value")

    SERVER_HOST = os.getenv("SERVER_HOST", None)

    if not SERVER_HOST:
        raise Exception("Generic exception about missing HOST value")

    SERVER_PORT = int(os.getenv("SERVER_PORT", 28960))

    app.config["RCON_PASSWORD"] = RCON_PASSWORD
    app.config["SERVER_HOST"] = SERVER_HOST
    app.config["SERVER_PORT"] = SERVER_PORT

    db.init_app(app)
    jwt.init_app(app)

    from models import User

    @app.cli.command("createdb")
    def create_db():
        db.create_all()
        print("Database schema created")

    @app.cli.command("createuser")
    @click.argument("username")
    @click.password_option()
    def create_user(username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"User {username} created")

    return app
