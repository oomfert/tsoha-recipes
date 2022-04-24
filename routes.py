from app import app
from db import db
from flask import render_template, redirect, request
import account
import recipes
import shopping


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recipe_list", methods=["GET"])
def recipe_list():
    if not account.account_id():
        print("session not recognized when trying to view recipes")
    else:
        return render_template("recipe_list.html", public_recipes=recipes.get_public_recipes(account.account_id()), private_recipes=recipes.get_private_recipes(account.account_id()))


@app.route("/recipe/<int:recipe_id>")
def open_recipe(recipe_id):
    data = recipes.get_recipe_data(recipe_id)
    return render_template("recipe.html", id=recipe_id, name=data[0], steps=data[1], ingredients=data[2])


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "GET":
        return render_template("add_recipe.html")
    if request.method == "POST":
        account.csrf_check()

        name = request.form["name"]
        steps = request.form["steps"]
        public = "public" in request.form
        ingredient_dict = {}
        try:
            for ingredient in request.form["ingredients"].split(","):
                ingredient_dict[ingredient.split(":")[0].strip()] = ingredient.split(":")[
                    1].strip()
        except:
            return render_template("add_recipe.html", error=True, errormsg="Adding recipe failed, make sure you used the correct ingredient format")

        recipes.add_recipe(name, ingredient_dict, steps,
                           account.account_id(), public)

        return redirect("/")

@app.route("/shopping_list", methods=["GET", "POST"])
def shopping_list():
    if request.method == "GET":
        if not account.account_id():
            print("session not recognized when trying to view shopping list")
        else:
            return render_template("shopping_list.html", list=shopping.get_shopping_list(account.account_id()))

@app.route("/recipe/<int:recipe_id>/add_to_list")
def recipe_to_list(recipe_id):
    if not account.account_id():
            print("session not recognized when trying to view shopping list")
    else:
        shopping.recipe_to_shopping_list(account.account_id(), recipe_id)
        return redirect("/shopping_list")



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
