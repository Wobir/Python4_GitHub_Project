from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.secret_key = 'asdasd'
db = SQLAlchemy(app)