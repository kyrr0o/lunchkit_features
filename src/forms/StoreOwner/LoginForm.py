from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
# from wtforms.validators import DataRequired, Email

class StoreOwnerLoginForm(FlaskForm):
    email = StringField('Email',[
        validators.DataRequired(),
        validators.Email(message="Invalid email address")
    ])

    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.Length(min=5,message="Password must be at least 8 characters")
    ])

