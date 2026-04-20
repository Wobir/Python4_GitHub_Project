from flask import Flask, render_template
from models import db, Users, Posts, Messages
from forms import RegForm, AuthForm, CreatePostForm
app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'


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
            email = request.form.get("email")
            if User.query.filter_by(name = name).first() or User.query.filter_by(email = email).first():
                message = "Пользователь с таким именем и почтой уже зарегестрирован"
                return render_template("reg.html", form = reg_form, message = message)
            new_user = User(
                name = name,
                email = email,
                password = password
            )

            db.session.add(new_user)
            db.session.commit()
    return render_template("reg.html", form = reg_form)

@app.route("/auth/", methods = ["POST", "GET"])
def auth():
    auth_form = AuthForm()
    if auth_form.validate_on_submit():
        if request.method=="POST":
            name=request.form.get("name")
            password= request.form.get("password")
            user = User.query.filter_by(name = name ).first()
            if not user:
                user = User.query.filter_by(email= name).first()
            if user and user.password == password:
                session["user_id"] = user.id
                session["user_name"] = user.name
                return redirect(url_for("index"))
            else:
                error = "Неверное имя пользователя или пароль"
                return render_template("auth.html", form = auth_form, error = error)
    return render_template ("auth.html", form = auth_form)



app.run(debug = True)