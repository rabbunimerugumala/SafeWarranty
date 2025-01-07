import traceback
import os
from flask import Flask, render_template, request, redirect, flash, url_for
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
# from schemas import RegisterWarrantyCard




# create a flask app
app = Flask(__name__)

app.secret_key = os.urandom(24)
# database connectivity
db_path = Path().cwd() / 'db/database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(db_path)

# Directory to save uploaded images
app.config['UPLOAD_FOLDER'] = 'static/uploads/' # Set the upload folder path
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class WarrantyCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=True)  # Path to the uploaded image
    product_name= db.Column(db.String(100), nullable=False)
    warranty_number = db.Column(db.String(80), unique=True ,nullable=False)
    product_purchase_date = db.Column(db.Date(), nullable=False)
    warranty_expiry_date = db.Column(db.Date(), nullable=False)
    warranty_provider = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



from wtforms import Form, StringField, validators, DateField, FileField

# schema class for Register student
class RegisterWarrantyCard(Form):
    image = FileField('Product Image')
    product_name = StringField('first_name',[validators.Length(min=2, max=50), validators.DataRequired()])
    warranty_number = StringField('last_name',[validators.Length(min=2, max=50), validators.DataRequired()])
    product_purchase_date = DateField('product_purchase_date' ,format="%Y-%m-%d")
    warranty_expiry_date = DateField('warranty_expiry_date' ,format="%Y-%m-%d")
    warranty_provider = StringField('warranty_Provider',[validators.Length(min=4, max=50), validators.DataRequired()])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_warranty', methods=('GET','POST'))
def add_warranty():
    form = RegisterWarrantyCard(request.form)

    if request.method == 'POST' and form.validate():
        try:
            # mapping the data from request form
            product_name: str = request.form.get('product_name', '').strip()
            warranty_number: str = request.form.get('warranty_number', '').strip()
            product_purchase_date: datetime = datetime.strptime(request.form.get('product_purchase_date').strip(),'%Y-%m-%d')
            warranty_expiry_date: datetime = datetime.strptime(request.form.get('warranty_expiry_date').strip(),'%Y-%m-%d')
            warranty_provider: str = request.form.get('warranty_provider', '').strip()
            # Retrieve the uploaded file
            image_file = request.files.get('image')
            filename = None  # Initialize filename
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                # Save the image to the UPLOAD_FOLDER
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
            # Create a new Warranty entry
            try:
                warranty_card = WarrantyCard(image=f"uploads/{filename}" if filename else None,product_name=product_name,warranty_number=warranty_number,product_purchase_date=product_purchase_date,warranty_expiry_date=warranty_expiry_date,warranty_provider=warranty_provider)
                db.session.add(warranty_card)
                db.session.commit()
                flash('Warranty card added  successfully!', 'success')
                return redirect(url_for('index'))
            # return render_template('warranty_mgmt/add_warranty.html',page_heading="Add a New Student", form=form, status="success")
            except IntegrityError:
                db.session.rollback()
                flash(f'An error occurred while adding the warranty card: {e}', 'danger')
        except Exception as e:
            traceback.print_exc()
            return render_template('warranty_mgmt/add_warranty.html',page_heading="Add a New Student", form=form, status="error")

    return render_template('warranty_mgmt/add_warranty.html', page_heading="Add a New Student",form=form )

# Route to display warranties
@app.route('/view_warranties/<int:warranty_id>')
def view_warranties(warranty_id):
    all_warranties = WarrantyCard.query.filter_by(id=warranty_id).first()
    return render_template('warranty_mgmt/view_warranty.html', page_heading='View Student Details', all_warranties=all_warranties)


@app.get('/get_warranties')
def get_warranties():
    try:
        # querying all the students
        warranties = WarrantyCard.query.all()

        # table headings
        headings = ("ID", "Image", "Product Name", "Warranty Number", "Purchase Date", "Expiry Date", "Provider")
        if warranties:
            return render_template('warranty_mgmt/warranties.html',page_heading='Students Details', headings=headings, warranties=warranties)
        else:
            return render_template('warranty_mgmt/warranties.html', warranties=[], message="No warranties found.")

    except Exception as e:
        traceback.print_exc()
        print(f'*** Error: Something went wrong while querying the student details from DB: {str(e)} ***')






# @app.route('/edit_warranty/<int:id>', methods=['GET', 'POST'])
# def edit_warranty(id):
#     warranty = Warranty.query.get_or_404(id)
#     form = WarrantyForm(obj=warranty)
#
#     if form.validate_on_submit():
#         # Handle image upload
#         image_file = request.files['image']
#         if image_file and allowed_file(image_file.filename):
#             filename = secure_filename(image_file.filename)
#             image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             image_file.save(image_path)
#             warranty.image = filename  # Save the image filename in the database
#
#         # Update other fields
#         warranty.product_name = form.product_name.data
#         warranty.warranty_number = form.warranty_number.data
#         warranty.product_purchase_date = form.product_purchase_date.data
#         warranty.warranty_expiry_date = form.warranty_expiry_date.data
#         warranty.warranty_provider = form.warranty_provider.data
#
#         db.session.commit()
#         return redirect('/warranties')
#
#     # Pass the URL of the existing image (if any) to the template
#     existing_image_url = url_for('static', filename=f'uploads/{warranty.image}') if warranty.image else None
#     return render_template('edit_warranty.html', form=form, existing_image_url=existing_image_url)
