from flask import Flask, render_template, request, redirect, url_for
from datetime import timedelta
from utils.extensions import db
from arena_interfaces.game_flask import game_flask
from menu_interfaces.menus import menus

import os

app = Flask(__name__)

app.register_blueprint(menus, url_prefix="/menus")
app.register_blueprint(game_flask, url_for="/game_flask")
app.permanent_session_lifetime = timedelta(minutes=5)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 5}
app.config['SECRET_KEY'] = "babati"

db.init_app(app)


@app.route("/", methods=["POST", "GET"])
def home() -> str:
    if request.method == "POST":
        return redirect(url_for("game_flask.arena")) # type: ignore
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
