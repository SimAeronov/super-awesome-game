from flask import Blueprint, render_template, Response, request
from game_engine import Game
import json
import time

game_flask = Blueprint("game_flask", __name__, static_folder="/static", template_folder="/templates")

NewGame = Game()
@game_flask.route("/arena", methods=["POST", "GET"])
def arena():
    if request.method == "POST":
        user_id = request.cookies.get('user_id')
        pressed_key = request.data.decode('UTF-8')
        NewGame.player_input(user_id=user_id, pressed_key=pressed_key)
        
    return render_template("arena_1.html") # type: ignore


@game_flask.route("/listen")
def listen():
    
    def respond_to_client():
        while True:
            players = NewGame.update_players_ui()
            # print(f"Updating: {players}")
            # players[0].player_coordinates_x
            # _data = json.dumps({"player": players[0].player_user_name, "location": players[0].player_coordinates_x})
            _data = json.dumps(players)
            print(f"Data that is being send: {_data}")
            yield f"id: 1\ndata: {str(_data)}\nevent: updatePlayers\n\n"
            time.sleep(0.9)
    return Response(respond_to_client(), mimetype='text/event-stream')
