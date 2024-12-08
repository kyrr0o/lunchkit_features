from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
import re


class PhMobileValidator:
    def __init__(self, message=None):
        self.message = message or 'Must be a valid Philippine mobile number (e.g., 09123456789)'

    def __call__(self, form, field):
        mobile = field.data
        # Check if starts with 09 and has exactly 11 digits
        if not re.match(r'^09\d{9}$', mobile):
            raise validators.ValidationError(self.message)


class StoreOwnerSignUpForm(FlaskForm):
    ownername = StringField('Owner name',[
        validators.DataRequired(),
        validators.Length(min=4,max=25,message="Name must be between 4 to 25 characters")
    ])

    email = StringField('Email',[
        validators.DataRequired(),
        validators.Email(message="Invalid email address")
    ])

    mobile = StringField('Mobile Number', [
        validators.DataRequired(),
        PhMobileValidator()
    ])

    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.Length(min=5,message="Password must be at least 8 characters"),
        validators.EqualTo('confirm_password',message='Passwords must match')
    ])

    confirm_password = PasswordField('Confirm Password')
