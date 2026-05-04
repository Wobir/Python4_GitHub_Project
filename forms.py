from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class RegForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Имя пользователя"})
    #email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "Электронная почта"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Пароль"})
    confirm_password = PasswordField("Confirm", validators=[DataRequired(), EqualTo("password")], render_kw={"placeholder": "Повтор пароля"})
    submit = SubmitField(render_kw={"value":"Зарегистрироваться"})
class AuthForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Имя пользователя или электронная почта"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Пароль"})
    submit = SubmitField(render_kw={"value":"Войти"})
class CreatePostForm(FlaskForm):
    image = FileField("PostContent" )
    text = TextAreaField("Text", render_kw={"placeholder":"Текст поста"})
    submit = SubmitField(render_kw={"value": "Создать пост"})