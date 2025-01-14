from wtforms import Form, StringField, validators, DateField, FileField
from wtforms.validators import DataRequired, InputRequired
from models import Category, Subcategory  # Import directly from models.py


# schema class for Register student
class RegisterWarrantyCard(Form):
    image = FileField('Product Image')
    # Category and Subcategory dropdowns
    category = StringField('Category', [validators.DataRequired()], render_kw={"readonly": True})  # Readonly
    subcategory = StringField('Subcategory', [validators.DataRequired()], render_kw={"readonly": True})  # Readonly
    product_name = StringField('first_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    warranty_number = StringField('last_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    product_purchase_date = DateField('product_purchase_date', format="%Y-%m-%d")
    warranty_expiry_date = DateField('warranty_expiry_date', format="%Y-%m-%d")
    warranty_provider = StringField('warranty_Provider', [validators.Length(min=4, max=50), validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        super(RegisterWarrantyCard, self).__init__(*args, **kwargs)
        self.category.choices = [(cat.id, cat.name) for cat in Category.query.all()]
        self.subcategory.choices = [(sub.id, sub.name) for sub in Subcategory.query.all()]


# Schema for edit student
class EditWarrantyCard(Form):
    image = FileField('Product Image')
    product_name = StringField('first_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    warranty_number = StringField('last_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    product_purchase_date = DateField('product_purchase_date', format="%Y-%m-%d")
    warranty_expiry_date = DateField('warranty_expiry_date', format="%Y-%m-%d")
    warranty_provider = StringField('warranty_Provider', [validators.Length(min=4, max=50), validators.DataRequired()])


# schema for search student
class SearchWarrantyForm(Form):
    warranty_product_name = StringField("warranty_product_name",
                                        [validators.Length(min=2, max=50), validators.DataRequired()])



from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterUserForm(FlaskForm):
    """
    Form to handle user registration with validation for username, email, and password.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(FlaskForm):
    """
    Form to handle user login with validation for username/email and password.
    """
    username = StringField('Username or Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

    submit = SubmitField('Login')

