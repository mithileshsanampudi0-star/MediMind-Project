from flask import Blueprint, render_template, request, redirect, session
from database.user_model import user_model

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        result = user_model.create_user(username, email, password)

        if result["success"]:
            return redirect("/login")

        return render_template("register.html", error=result["message"])

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = user_model.authenticate_user(email, password)

        if user:
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            return redirect("/")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()
    return redirect("/login")