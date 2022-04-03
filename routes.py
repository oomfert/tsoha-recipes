from app import app
from db import db
from flask import render_template, redirect, request
import account


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if account.login(username, password):
        return redirect("/")
    else:
        return render_template("index.html", error=True, errormsg="Login failed")


@app.route("/logout")
def logout():
    account.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_again = request.form["password_again"]
        if password != password_again:
            return render_template("register.html", error=True, errormsg="Passwords do not match")
        account.register(username, password)
        return redirect("/")
