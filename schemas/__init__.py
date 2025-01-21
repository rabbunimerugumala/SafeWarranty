"""
This file defines form schemas for the application using Flask-WTF and WTForms.
It includes validation and structure for forms related to user registration, login, warranty card registration,
editing, and searching.

Key Features:
1. **RegisterWarrantyCard**: Form for adding warranty cards with fields for product details and category/subcategory selection.
2. **EditWarrantyCard**: Form for editing warranty card details.
3. **SearchWarrantyForm**: Form for searching warranty cards by product name.
4. **RegisterUserForm**: Form for registering new users with validation for username, email, and password.
5. **LoginForm**: Form for user login with validation for credentials.
"""

from flask_wtf.file import FileField  # For file uploads
# Import necessary libraries for form creation and validation
from wtforms import Form, StringField, DateField  # Form fields for input
from wtforms.validators import DataRequired, InputRequired, Length  # Validators for form fields

# Import models to dynamically fetch category and subcategory data
from models import Category, Subcategory


# Schema for registering a warranty card
class RegisterWarrantyCard(Form):
    """
    Form for registering a new warranty card.
    Includes fields for product details, category, subcategory, and optional image upload.
    """
    image = FileField('Product Image')  # Optional product image file upload
    category = StringField(
        'Category',
        [DataRequired()],
        render_kw={"readonly": True}  # Dropdown for category selection, readonly
    )
    subcategory = StringField(
        'Subcategory',
        [DataRequired()],
        render_kw={"readonly": True}  # Dropdown for subcategory selection, readonly
    )
    product_name = StringField(
        'Product Name',
        [Length(min=2, max=50), DataRequired()]  # Product name with validation for length and presence
    )
    warranty_number = StringField(
        'Warranty Number',
        [Length(min=2, max=50), DataRequired()]  # Unique warranty number with validation
    )
    product_purchase_date = DateField(
        'Purchase Date',
        format="%Y-%m-%d"  # Date of purchase in YYYY-MM-DD format
    )
    warranty_expiry_date = DateField(
        'Expiry Date',
        format="%Y-%m-%d"  # Date of warranty expiration in YYYY-MM-DD format
    )
    warranty_provider = StringField(
        'Warranty Provider',
        [Length(min=4, max=50), DataRequired()]  # Provider of the warranty with validation
    )

    def __init__(self, *args, **kwargs):
        """
        Custom initialization to populate category and subcategory dropdowns dynamically.
        """
        super(RegisterWarrantyCard, self).__init__(*args, **kwargs)
        # Dynamically fetch categories and subcategories from the database
        self.category.choices = [(cat.id, cat.name) for cat in Category.query.all()]
        self.subcategory.choices = [(sub.id, sub.name) for sub in Subcategory.query.all()]


# Schema for editing warranty card details
class EditWarrantyCard(Form):
    """
    Form for editing an existing warranty card.
    Includes fields for updating product details and image.
    """
    image = FileField('Product Image')  # Optional product image file upload
    product_name = StringField(
        'Product Name',
        [Length(min=2, max=50), DataRequired()]  # Validation for product name
    )
    warranty_number = StringField(
        'Warranty Number',
        [Length(min=2, max=50), DataRequired()]  # Validation for unique warranty number
    )
    product_purchase_date = DateField(
        'Purchase Date',
        format="%Y-%m-%d"  # Date of purchase in YYYY-MM-DD format
    )
    warranty_expiry_date = DateField(
        'Expiry Date',
        format="%Y-%m-%d"  # Date of warranty expiration in YYYY-MM-DD format
    )
    warranty_provider = StringField(
        'Warranty Provider',
        [Length(min=4, max=50), DataRequired()]  # Validation for provider name
    )


# Schema for searching warranty cards
class SearchWarrantyForm(Form):
    """
    Form for searching warranty cards by product name.
    """
    warranty_product_name = StringField(
        "Warranty Product Name",
        [Length(min=2, max=50), DataRequired()]  # Validation for search input
    )


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# Schema for registering new users
class RegisterUserForm(FlaskForm):
    """
    Form for registering a new user.
    Includes fields for username, email, and password with validation.
    """
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=4, max=20)]  # Username validation for presence and length
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]  # Validation for email format
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)]  # Password validation for presence and minimum length
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]  # Validation to match the password field
    )

    submit = SubmitField('Register')  # Submit button for the form


# Schema for user login
class LoginForm(FlaskForm):
    """
    Form for logging in an existing user.
    Includes fields for username or email and password.
    """
    username = StringField(
        'Username or Email',
        validators=[InputRequired()]  # Validation for presence
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired()]  # Validation for presence
    )

    submit = SubmitField('Login')  # Submit button for the form
