from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, validators


class StoreRegistrationForm(FlaskForm):
    store_name = StringField('Store name',[
        validators.DataRequired(),
        validators.Length(min=4,max=50)
    ])

    email = StringField('Email',[
        validators.DataRequired(),
        validators.Email()
    ])

    sanitary_permit = FileField('Sanitary permit to Operate', validators=[
        FileRequired(),
        FileAllowed(['jpg','jpeg','png'], 'Only Jpeg, Jpg and png file extensions are allowed')
    ])

    certificate_of_business_name_registration = FileField('Certificate of Business Name Registration', validators=[
        FileRequired(),
        FileAllowed(['jpg','jpeg','png'], 'Only Jpeg, Jpg and png file extensions are allowed')
    ])

    business_permit = FileField('Business Permit', validators=[
        FileRequired(),
        FileAllowed(['jpg','jpeg','png'], 'Only Jpeg, Jpg and png file extensions are allowed')
    ])

    fire_safety_inspection_certificate = FileField('Fire Safety Inspection Inspection Certificate', validators=[
        FileRequired(),
        FileAllowed(['jpg','jpeg','png'], 'Only Jpeg, Jpg and png file extensions are allowed')
    ])

    certificate_of_registration = FileField('Certificate of Registration', validators=[
        FileRequired(),
        FileAllowed(['jpg','jpeg','png'], 'Only Jpeg, Jpg and png file extensions are allowed')
    ])

    tax_payment_form = FileField('Tax Payment Form', validators=[
        FileRequired(),
        FileAllowed(['jpg','jpeg','png'], 'Only Jpeg, Jpg and png file extensions are allowed')
    ])