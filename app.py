from flask import Flask
from flask import jsonify
from dotenv import load_dotenv
from dotenv import find_dotenv
from backend import models
import os

load_dotenv(find_dotenv())

app = Flask(__name__)

RCON_PASS = os.getenv('RCON_PASS', None)

if not RCON_PASS:
    raise Exception('Generic exception about missing rcon pass')

SERVER_HOST = os.getenv('SERVER_HOST', None)

if not SERVER_HOST:
    raise Exception('Generic exception about missing HOST value')

SERVER_PORT = int(os.getenv('SERVER_PORT', 28960))

if not SERVER_PORT:
    raise Exception('Generic exception about missing PORT value')

def check_user_authenticated(rcon_password):  ### To use with simple auth check on each restricted endpoint
    return rcon_password == RCON_PASS

@app.route("/")
def home():
    return "Hello"


@app.route("/players")
def get_players():

    ### TODO: Implement auth check here

    rcon = models.RCON(SERVER_HOST, SERVER_PORT, RCON_PASS)

    players = {}

    try:
        players = rcon.status()
        print(str(players))
    except Exception as e:
        print(str(e))
        print('Add proper exception handling here for exceptions of UDP socket or other failure')
        return jsonify({}), 500

    return jsonify(players), 200


@app.route("/playerkick/<int:player_num>")
def player_kick(player_num):
    print('Trying to kick: ' + player_num)
    rcon = models.RCON(SERVER_HOST, SERVER_PORT, RCON_PASS)
    rcon.kick(player_num)

    return jsonify({}), 200
