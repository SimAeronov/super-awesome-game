from flask import Blueprint, render_template, request
from game_engine import Game
import json

game_flask = Blueprint("game_flask", __name__, static_folder="/static", template_folder="/templates")

NewGame = Game()
@game_flask.route("/arena_1", methods=["POST", "GET"])
def arena():
    return render_template("arena_1.html") # type: ignore


@game_flask.route("/listen", methods=['GET','POST']) # type: ignore
def listen():
    if request.method=='GET':
        players = NewGame.update_players_ui()
        _data = json.dumps(players)
        print(f"Data that is being send: {_data}")
        return _data
    elif request.method=='POST':
        user_id = request.cookies.get('user_id')
        pressed_key = request.data.decode('UTF-8')
        NewGame.player_input(user_id=user_id, pressed_key=pressed_key)
        return render_template("arena_1.html") # type: ignore
