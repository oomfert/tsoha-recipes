from db import db
import recipes

def get_shopping_list(account_id):
    sql = "SELECT list FROM shoppinglists WHERE creator_id = :account_id"
    list_string = db.session.execute(sql, {"account_id": account_id}).fetchone()
    if list_string == None:
        init_shopping_list(account_id)
        list_string = db.session.execute(sql, {"account_id": account_id}).fetchone()
        return list_string[0]
    else:
        print(list_string[0])
        return list_string[0]

def init_shopping_list(account_id):
    sql = "INSERT INTO shoppinglists (creator_id, list) VALUES (:creator_id, 'Placeholder')"
    db.session.execute(sql, {"creator_id": account_id})
    db.session.commit()

def update_shopping_list(account_id, text):
    pass

def recipe_to_shopping_list(account_id, recipe_id):
    recipe_string = ""
    for key, value in recipes.get_recipe_data(recipe_id)[2].items():
        recipe_string += f"{key} {value}, "
    new_list = f"{get_shopping_list(account_id)}, {recipe_string}"    #TODO: make this formatted in a way where i can display one ingredient per line in the html template      
    sql = "UPDATE shoppinglists SET list = :new_list WHERE creator_id = :creator_id"
    db.session.execute(sql, {"new_list": new_list, "creator_id": account_id})
    db.session.commit()



    

