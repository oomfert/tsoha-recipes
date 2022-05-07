import secrets
from db import db
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password FROM accounts WHERE username=:username"
    account = db.session.execute(sql, {"username": username}).fetchone()
    if not account:
        return False
        print("acc not in db")
    else:
        passhash = account[1]
        if check_password_hash(passhash, password):
            session["account_id"] = account[0]
            session["username"] = username
            return True
        else:
            return False
            print("passhash wrong")


def logout():
    session.clear()


def register(username, password):
    passhash = generate_password_hash(password)
    sql = "INSERT INTO accounts (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username": username, "password": passhash})
    db.session.commit()
    return login(username, password)

def account_id():
    return session.get("account_id", 0)
