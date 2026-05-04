from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["UPLOAD_FOLDER"] = "static/user_content/"
app.secret_key = 'asdasd'
