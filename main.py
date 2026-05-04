from flask import Flask, render_template, request, redirect, url_for, session
from models import *
from forms import RegForm, AuthForm, CreatePostForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from modules import *
import bcrypt
import os

def hash_password(password : str):
    salt = bcrypt.gensalt(rounds=14)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password_input : str, hashed_password : str):
    return bcrypt.checkpw(password_input.encode("utf-8"), hashed_password.encode("utf-8"))



check_db()

@app.route("/base/")
def base():
    return render_template("base.html")

@app.route("/reg/", methods =["GET", "POST"])
def reg():
    
    reg_form = RegForm()
    if reg_form.validate_on_submit():
        if request.method == "POST":
            
            name = request.form.get("name")
            password = request.form.get("password")
            #email = request.form.get("email")
            if find_user_by_name(name): #Users.query.filter_by(name = name).first() or Users.query.filter_by(email = email).first():
                message = "Пользователь с таким лоигном уже зарегестрирован"
                return render_template("reg.html", form = reg_form, message = message)
            new_user = Users(
                name = name,
                password = hash_password(password)
            )
            create_user(new_user)
    return render_template("reg.html", form = reg_form)

@app.route("/login/", methods = ["POST", "GET"])
def auth():
    if "user_name" in session:
        return redirect(url_for("profile"))
    auth_form = AuthForm()
    if auth_form.validate_on_submit():
        if request.method=="POST":
            name=request.form.get("name")
            password= request.form.get("password")
            user = find_user_by_name(name)
            if not user:
                user = find_user_by_email(name)
            if user and verify_password(password, user.password):
                session["user_id"] = user.id
                session["user_name"] = user.name
                return redirect(url_for("index"))
            else:
                error = "Неверное имя пользователя или пароль"
                return render_template("auth.html", form = auth_form, error = error)
    return render_template ("auth.html", form = auth_form)

@app.route("/profile/", methods = ["POST", 'GET'])
def profile():
    form = CreatePostForm()
    user = find_user_by_name(session["user_name"])
    if request.method == "POST":
        text = request.form.get("text")
        image = request.files["image"]
        if not text and not image:
            return render_template("profile.html", user = user, form = form, message = "Пост не создан так как нечего создавать")
        if text:
            create_post(id = session["user_id"], text=text)
        elif image:
            filename = session["user_name"] +"."+ image.filename.split(".")[-1]
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            create_post(id = session["user_id"], image = filename)
    return render_template("profile.html", user = user, form = form)

@app.route("/news/")
def news():
    posts = find_all_posts()
    return render_template("news.html", posts = posts)

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug=True)


