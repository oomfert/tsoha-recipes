from app import app
from os import getenv
import re

from flask_sqlalchemy import SQLAlchemy

uri = getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
db = SQLAlchemy(app)
db.create_all()
