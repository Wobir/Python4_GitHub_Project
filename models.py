from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"))
    name = db.Column(db.String())
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.Text, nullable=False)