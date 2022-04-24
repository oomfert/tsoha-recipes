from db import db


def get_public_recipes(account_id):
    sql = "SELECT id, name, creator_id FROM recipes WHERE (public = TRUE AND visible = TRUE) ORDER BY creator_id = :account_id DESC, name ASC"
    return db.session.execute(sql, {"account_id": account_id}).fetchall()

def get_private_recipes(account_id):
    sql = "SELECT id, name FROM recipes WHERE (public = FALSE AND visible = TRUE AND creator_id = :account_id) ORDER BY name ASC"
    return db.session.execute(sql, {"account_id": account_id}).fetchall()


def get_recipe_data(recipe_id):
    sql = """SELECT recipes.name, recipes.steps, ingredients.name, quantities.amount 
            FROM recipes, ingredients, quantities
            WHERE (recipes.visible = TRUE AND recipes.id = :recipe_id AND quantities.recipe_id = :recipe_id AND quantities.ingredient_id = ingredients.id)"""
    result = db.session.execute(sql, {"recipe_id": recipe_id}).fetchall()
    ingredient_dict = {}
    name = result[0][0]
    steps = result[0][1]
    for row in result:
        ingredient_dict[row[2]] = row[3]
    return name, steps, ingredient_dict


def add_recipe(name, ingredients: dict, steps, account_id, public):
    sql_recipes = "INSERT INTO recipes (creator_id, name, steps, public, visible) VALUES (:creator_id, :name, :steps, :public, TRUE) RETURNING id"
    recipe_id = db.session.execute(sql_recipes, {
                                   "creator_id": account_id, "name": name, "steps": steps, "public": public}).fetchone()[0]
    sql_ingredients = "INSERT INTO ingredients (name, visible) VALUES (:ingredient, TRUE) RETURNING ID"
    sql_quantities = "INSERT INTO quantities (recipe_id, ingredient_id, amount) VALUES (:recipe_id, :ingredient_id, :amount)"
    for item in ingredients.items():
        ingredient_id = db.session.execute(
            sql_ingredients, {"ingredient": item[0]}).fetchone()[0]
        db.session.execute(sql_quantities, {
                           "recipe_id": recipe_id, "ingredient_id": ingredient_id, "amount": item[1]})
    db.session.commit()
