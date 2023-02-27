from flask import Blueprint, render_template,request, redirect, url_for, session, flash, Response
from typing import Optional, Union
from utils.extensions import db

menus = Blueprint("menus", __name__, static_folder="/static", template_folder="/templates")


class users(db.Model): # type: ignore 
    _id = db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    player_name = db.Column(db.String(100))

    def __init__(self, user_name:str, player_name:Optional[str]):
        self.user_name = user_name
        self.player_name = player_name

@menus.route("/scores")
def scores():
    return render_template("scores.html", values=users.query.all()) # type: ignore 

@menus.route("/login", methods=["POST", "GET"])
def login() -> str:
    if request.method == "POST":
        session.permanent = True
        user:str = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(user_name=user).first() # type: ignore 
        if found_user:
            session["player_name"] = found_user.player_name # type: ignore 
        else:
            usr = users(user_name=user, player_name=None)
            db.session.add(usr) # type: ignore 
            db.session.commit() # type: ignore 

        flash(f"Logged in as: {user}", "info")
        response = redirect(url_for("menus.user"))
        response.set_cookie('user_id', user)
        return response
    else:
        if "user" in session:
            flash("Already logged in", "info")
            return redirect(url_for("menus.user")) # type: ignore  
        return render_template("login.html")

@menus.route("/user", methods=["POST", "GET"])
def user() -> str:
    player_name:Optional[str] = None
    if "user" in session:
        user: str = session["user"]

        if request.method == "POST":
            player_name = request.form["player_name"]
            session["player_name"] = player_name
            found_user = users.query.filter_by(user_name=user).first() # type: ignore 
            found_user.player_name = player_name
            db.session.commit() # type: ignore 
        else:
            if "player_name" in session:
                player_name = session["player_name"]
        return render_template("user.html", user=player_name)
    else:
        return redirect(url_for("menus.login")) # type: ignore 

@menus.route("/logout")
def logout():
    session.pop("user", None)# type: ignore
    session.pop("player_name", None)# type: ignore
    return redirect(url_for("menus.login"))