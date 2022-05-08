from db import db
import recipes


def get_shopping_list(account_id):
    sql = "SELECT ingredient, amount FROM shoppinglists WHERE creator_id = :account_id"
    return db.session.execute(sql, {"account_id": account_id}).fetchall()


def update_shopping_list(account_id, text):
    pass


def recipe_to_shopping_list(account_id, recipe_id):
    for key, value in recipes.get_recipe_data(recipe_id)[2].items():
        sql = "INSERT INTO shoppinglists (creator_id, ingredient, amount, visible) VALUES (:creator_id, :ingredient, :amount, TRUE)"
        db.session.execute(
            sql, {"creator_id": account_id, "ingredient": key, "amount": value})
    db.session.commit()
