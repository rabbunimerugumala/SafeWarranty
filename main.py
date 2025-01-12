import traceback
import os
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from schemas import RegisterWarrantyCard, EditWarrantyCard

# create a flask app
app = Flask(__name__)

app.secret_key = os.urandom(24)
# database connectivity
db_path = Path().cwd() / 'db/database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(db_path)

# Directory to save uploaded images
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Set the upload folder path
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import WarrantyCard


# Allowed file extensions for images
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Main types and subcategories data
categories = {
    "Electronics Warranty": ["Smartphones", "Laptops", "Tablets", "Cameras", "Headphones", "Wearables", "Others"],
    "Home Appliances Warranty": ["Refrigerators", "Washing Machines", "Microwave Ovens", "Air Conditioners",
                                 "Vacuum Cleaners", "Coffee Machines", "Others"],
    "Automobile Warranty": ["Cars", "Motorcycles", "Electric Scooters", "Bicycles", "Spare Parts", "Others"],
    "Furniture Warranty": ["Sofas", "Beds", "Tables and Chairs", "Wardrobes", "Mattresses", "Others"],
    "Office Equipment": ["Printers", "Computers and Accessories", "Desks and Chairs", "Projectors", "Others"],
    "Tools & Machinery": ["Power Tools", "Hand Tools", "Garden Equipment", "Workshop Machines", "Others"],
    "Other Warranties": ["Musical Instruments", "Sports Equipment", "Toys", "Tools", "Miscellaneous", "Others"],
}


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/add_warranty')
# def warranty_categories():
#     # Fetch all categories from the database
#     categories = Category.query.all()
#     print(categories)  # Check if categories are fetched correctly
#     # Pass the categories to the template to render as cards
#     return render_template('warranty_mgmt/add_warranty/categories_page.html', categories=categories)
#
#
# @app.route('/subcategories/<category_id>', methods=['GET'])
# def subcategories(category_id):
#     # Get subcategories dynamically based on selected category
#     category = Category.query.get(category_id)
#     if not category:
#         return jsonify({"error": "Category not found"}), 404
#
#     subcategories = Subcategory.query.filter_by(category_id=category_id).all()
#     subcategory_list = [{"id": sub.id, "name": sub.name} for sub in subcategories]
#     return jsonify({"subcategories": subcategory_list})


@app.route('/add_warranty', methods=('GET', 'POST'))
def add_warranty():
    form = RegisterWarrantyCard(request.form)
    if request.method == 'POST' and form.validate():
        try:
            product_name = request.form.get('product_name', '').strip()
            warranty_number = request.form.get('warranty_number', '').strip()
            product_purchase_date = datetime.strptime(request.form.get('product_purchase_date').strip(), '%Y-%m-%d')
            warranty_expiry_date = datetime.strptime(request.form.get('warranty_expiry_date').strip(), '%Y-%m-%d')
            warranty_provider = request.form.get('warranty_provider', '').strip()

            # File upload handling
            image_file = request.files.get('image')
            warranty_image = None  # Default to no image

            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                warranty_image = f"uploads/{filename}"  # Save relative path
            else:
                flash("Invalid or missing image file. Please upload a valid image (png, jpg, jpeg, gif).", "danger")
                return render_template(
                    'warranty_mgmt/add_warranty/warranty_form.html',

                )
            try:
                # Add new warranty card to the database
                warranty_card = WarrantyCard(
                    image=warranty_image,
                    product_name=product_name,
                    warranty_number=warranty_number,
                    product_purchase_date=product_purchase_date,
                    warranty_expiry_date=warranty_expiry_date,
                    warranty_provider=warranty_provider

                )

                db.session.add(warranty_card)
                db.session.commit()
                flash('Warranty card added successfully!', 'success')
                return redirect(url_for('get_warranties'))

            except IntegrityError as e:
                db.session.rollback()
                flash(f'An error occurred while adding the warranty card: {e}', 'danger')
        except Exception as e:
            traceback.print_exc()
            flash(f'An unexpected error occurred: {e}', 'danger')

    return render_template('warranty_mgmt/add_warranty/warranty_form.html',page_heading="Add Warranty",form=form)



# Route to display warranties
@app.route('/view_warranties/<int:warranty_id>')
def view_warranties(warranty_id):
    all_warranties = WarrantyCard.query.filter_by(id=warranty_id).first()
    return render_template('warranty_mgmt/view_warranty.html', page_heading='View Warranty Details',all_warranties=all_warranties)


@app.get('/get_warranties')
def get_warranties():
    try:
        # querying all the students
        warranties = WarrantyCard.query.all()
        if warranties:
            return render_template('warranty_mgmt/warranties.html', page_heading='Warranty Details',
                                   warranties=warranties)
        else:
            return render_template('warranty_mgmt/warranties.html', warranties=[], message="No warranties found.")

    except Exception as e:
        traceback.print_exc()
        print(f'*** Error: Something went wrong while querying the student details from DB: {str(e)} ***')


@app.route('/edit_warranty/<int:warranty_id>', methods=['GET', 'POST'])
def edit_warranty(warranty_id):
    # Fetch the warranty card from the database by ID, or return a 404 error if not found
    warranty = WarrantyCard.query.get_or_404(warranty_id)

    # Initialize the form with the current warranty data
    form = EditWarrantyCard(request.form)

    if request.method == 'POST' and form.validate():
        try:
            # Handle image upload
            image_file = request.files.get('image')  # Get the uploaded file from the form
            if image_file and allowed_file(image_file.filename):  # Check if the file is valid
                filename = secure_filename(image_file.filename)  # Secure the filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Define the upload path
                image_file.save(image_path)  # Save the uploaded file to the server
                warranty.image = filename  # Update the warranty record with the new image filename

            # Update other fields with the form data
            warranty.product_name = form.product_name.data  # Update product name
            warranty.warranty_number = form.warranty_number.data  # Update warranty number
            warranty.product_purchase_date = form.product_purchase_date.data  # Update purchase date
            warranty.warranty_expiry_date = form.warranty_expiry_date.data  # Update expiry date
            warranty.warranty_provider = form.warranty_provider.data  # Update warranty provider

            # Commit the changes to the database
            db.session.commit()
            flash("Warranty updated successfully!", "success")  # Show a success message
            # redirect to students page
            return render_template('warranty_mgmt/edit_warranty.html', page_heading='Edit Warranty Details',
                                   warranty=warranty, status="success", form=form)
            # return redirect('/get_warranties')  # Redirect to the list of warranties

        except Exception as e:
            # Roll back the database session to avoid partial changes
            db.session.rollback()
            # Log the error for debugging (optional)
            # Show an error message to the user
            flash("An error occurred while updating the warranty. Please try again.", "danger")

    # Generate the URL of the existing image if available
    existing_image_url = url_for('static', filename=f'uploads/{warranty.image}') if warranty.image else None

    # Render the edit warranty template and pass the form and existing image URL
    return render_template('warranty_mgmt/edit_warranty.html', form=form, existing_image_url=existing_image_url,
                           warranty=warranty)


@app.post('/delete_warranty/<int:warranty_id>')
def delete_warranty(warranty_id):
    warranty = WarrantyCard.query.get_or_404(warranty_id)
    db.session.delete(warranty)
    db.session.commit()
    return redirect(url_for('get_warranties'))
