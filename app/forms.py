from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名。')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码。')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(), 
        Length(min=6, message='用户名长度不能少于6个字节。')
    ])
    email = StringField('电子邮箱', validators=[
        DataRequired(), 
        Email(message='请输入有效的Email地址。')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(),
        Length(min=6, message='密码长度不能少于6个字节。')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(), 
        EqualTo('password', message='两次输入的密码不一致。')
    ])
    submit = SubmitField('注册')

    # 验证用户名唯一性 
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被注册。')

    # 验证 Email 唯一性 
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该Email地址已被注册。')