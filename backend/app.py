from flask import Flask
from flask import jsonify
from dotenv import load_dotenv
from dotenv import find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello"


@app.route("/players")
def get_players():
    players = [
        {
            "num": 0,
            "name": "ZED",
            "score": 14,
            "address": "8.8.8.8",
            "rate": 25000,
            "ping": 75,
        },
        {
            "num": 1,
            "name": "FMM",
            "score": 14,
            "address": "1.1.1.1",
            "rate": 5000,
            "ping": 60,
        },
    ]
    return jsonify(players), 200


@app.route("/playerkick/<int:player_num>")
def player_kick(player_num):
    print(player_num)
    return jsonify({}), 200
