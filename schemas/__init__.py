from wtforms import Form, StringField, validators, DateField, FileField, SelectField
from wtforms.validators import DataRequired


# schema class for Register student
class RegisterWarrantyCard(Form):
    image = FileField('Product Image')
    # category = SelectField('Category', coerce=int, validators=[DataRequired()])
    # subcategory = SelectField('Subcategory', coerce=int, validators=[DataRequired()])
    product_name = StringField('first_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    warranty_number = StringField('last_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    product_purchase_date = DateField('product_purchase_date', format="%Y-%m-%d")
    warranty_expiry_date = DateField('warranty_expiry_date', format="%Y-%m-%d")
    warranty_provider = StringField('warranty_Provider', [validators.Length(min=4, max=50), validators.DataRequired()])


# Schema for edit student
class EditWarrantyCard(Form):
    image = FileField('Product Image')
    product_name = StringField('first_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    warranty_number = StringField('last_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    product_purchase_date = DateField('product_purchase_date', format="%Y-%m-%d")
    warranty_expiry_date = DateField('warranty_expiry_date', format="%Y-%m-%d")
    warranty_provider = StringField('warranty_Provider', [validators.Length(min=4, max=50), validators.DataRequired()])
