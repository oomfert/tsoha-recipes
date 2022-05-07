from flask import Flask
from flask_wtf.csrf import CSRFProtect
from os import getenv

csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
csrf.init_app(app)

import routes