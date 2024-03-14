#!/usr/bin/python3
"""forms for login"""
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
class LoginForm(FlaskForm):
    username=StringField('username',
                         validators=[DataRequired(), Length(min=2,max=20)])
    email=EmailField('email', validators=[DataRequired(), Email()])
    password=PasswordField('password', validators=[DataRequired()])
    remember=BooleanField('Remember me')
    login=SubmitField('login')