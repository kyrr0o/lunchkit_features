'''
This is Flask WTForms class.
Whenever you're creating a form, you use these methods to your routes.
You only need one instance of this class to be stored in a variable for a specific route.
Call the variable with Jinja and then render it to the html files.
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, DecimalField, HiddenField
from wtforms.validators import DataRequired

class AddItem(FlaskForm):
    itemName = StringField("Enter Item Name", 
                            validators=[DataRequired()])
    
    itemDesc = TextAreaField("Enter Item Description", 
                              validators=[DataRequired()])
    
    itemPrice = DecimalField("Enter Item Price", 
                              validators=[DataRequired()])
    
    itemPhoto = FileField("Upload Item Photo", 
                           validators=[DataRequired()])
    
    StoreId = HiddenField(validators=[DataRequired()])
    
    submit = SubmitField("Submit")
    