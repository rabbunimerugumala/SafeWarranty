from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import WarrantyCard, Category, Subcategory, db
from schemas import RegisterWarrantyCard, EditWarrantyCard, SearchWarrantyForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

warranty_mgmt = Blueprint('warranty_mgmt', __name__)

# Helper function to check allowed file types
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@warranty_mgmt.route('/index')
@login_required
def index():
    print(f"Is user authenticated: {current_user.is_authenticated}")
    return render_template('index.html')

@warranty_mgmt.route('/add_warranty')
@login_required
def categories_page():
    categories = Category.query.all()
    return render_template('warranty_mgmt/add_warranty/categories_page.html', categories=categories)

@warranty_mgmt.route('/subcategories/<int:category_id>')
@login_required
def subcategories_page(category_id):
    category = Category.query.get_or_404(category_id)
    subcategories = Subcategory.query.filter_by(category_id=category.id).all()
    return render_template('warranty_mgmt/add_warranty/subcategories.html', category=category,
                           subcategories=subcategories)

@warranty_mgmt.route('/warranty_form', methods=('GET', 'POST'))
@login_required
def add_warranty():
    subcategory_id = request.args.get('subcategory_id', type=int)
    if not subcategory_id:
        flash("Invalid subcategory. Please select a valid subcategory.", "danger")
        return redirect(url_for('warranty_mgmt.categories_page'))

    subcategory = Subcategory.query.get_or_404(subcategory_id)
    category = Category.query.get_or_404(subcategory.category_id)

    form = RegisterWarrantyCard(request.form)

    # Pre-fill the category and subcategory in the form
    form.category.data = category.id
    form.subcategory.data = subcategory.id

    if request.method == 'POST' and form.validate():
        try:
            # Get form data
            product_name = request.form.get('product_name', '').strip()
            warranty_number = request.form.get('warranty_number', '').strip()
            product_purchase_date = datetime.strptime(request.form.get('product_purchase_date').strip(), '%Y-%m-%d')
            warranty_expiry_date = datetime.strptime(request.form.get('warranty_expiry_date').strip(), '%Y-%m-%d')
            warranty_provider = request.form.get('warranty_provider', '').strip()

            # Check for duplicate warranty
            existing_warranty = WarrantyCard.query.filter_by(
                warranty_number=warranty_number,
                product_name=product_name,
                category_id=category.id,
                subcategory_id=subcategory.id
            ).first()

            if existing_warranty:
                flash("This warranty already exists in the database.", "danger")
                return render_template(
                    'warranty_mgmt/add_warranty/warranty_form.html',
                    form=form,
                    category=category,
                    subcategory=subcategory,
                    page_heading="Add Warranty"
                )

            # File upload handling
            image_file = request.files.get('image')
            warranty_image = None  # Default to no image

            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join('static/uploads', filename)
                image_file.save(image_path)
                warranty_image = f"uploads/{filename}"  # Save relative path
            else:
                flash("Invalid or missing image file. Please upload a valid image (png, jpg, jpeg, gif).", "danger")
                return render_template(
                    'warranty_mgmt/add_warranty/warranty_form.html',
                    form=form,
                    category=category,
                    subcategory=subcategory,
                    page_heading="Add Warranty"
                )

            # Add new warranty card to the database
            warranty_card = WarrantyCard(
                image=warranty_image,
                product_name=product_name,
                warranty_number=warranty_number,
                product_purchase_date=product_purchase_date,
                warranty_expiry_date=warranty_expiry_date,
                warranty_provider=warranty_provider,
                category_id=category.id,
                subcategory_id=subcategory.id
            )

            db.session.add(warranty_card)
            db.session.commit()
            flash('Warranty card added successfully!', 'success')
            return redirect(url_for('warranty_mgmt.get_warranties'))

        except Exception as e:
            flash(f'An error occurred while adding the warranty card: {e}', 'danger')

    return render_template(
        'warranty_mgmt/add_warranty/warranty_form.html',
        form=form,
        category=category,
        subcategory=subcategory,
        page_heading="Add Warranty"
    )

@warranty_mgmt.route('/view_warranties/<int:warranty_id>')
@login_required
def view_warranties(warranty_id):
    all_warranties = WarrantyCard.query.filter_by(id=warranty_id).first()
    return render_template('warranty_mgmt/view_warranty.html', page_heading='View Warranty Details',
                           all_warranties=all_warranties)


@warranty_mgmt.route('/get_warranties')
@login_required
def get_warranties():
    warranties = WarrantyCard.query.all()
    return render_template('warranty_mgmt/warranties.html', page_heading='Warranty Details', warranties=warranties)


@warranty_mgmt.route('/edit_warranty/<int:warranty_id>', methods=['GET', 'POST'])
@login_required
def edit_warranty(warranty_id):
    warranty = WarrantyCard.query.get_or_404(warranty_id)
    form = EditWarrantyCard(request.form)

    if request.method == 'POST' and form.validate():
        try:
            # Handle image upload
            image_file = request.files.get('image')
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join('static/uploads', filename)
                image_file.save(image_path)
                warranty.image = filename

            # Update other fields with the form data
            warranty.product_name = form.product_name.data
            warranty.warranty_number = form.warranty_number.data
            warranty.product_purchase_date = form.product_purchase_date.data
            warranty.warranty_expiry_date = form.warranty_expiry_date.data
            warranty.warranty_provider = form.warranty_provider.data

            db.session.commit()
            flash("Warranty updated successfully!", "success")
            return redirect(url_for('warranty_mgmt.get_warranties'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error updating warranty: {e}", "danger")

    existing_image_url = url_for('static', filename=f'uploads/{warranty.image}') if warranty.image else None
    return render_template('warranty_mgmt/edit_warranty.html', form=form, existing_image_url=existing_image_url, warranty=warranty)


@warranty_mgmt.route('/delete_warranty/<int:warranty_id>', methods=['POST'])
@login_required
def delete_warranty(warranty_id):
    warranty = WarrantyCard.query.get_or_404(warranty_id)
    try:
        db.session.delete(warranty)
        db.session.commit()
        flash('Warranty deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting warranty: {e}', 'danger')
    return redirect(url_for('warranty_mgmt.get_warranties'))


@warranty_mgmt.route('/search_warranties', methods=['GET', 'POST'])
@login_required
def search_warranties():
    form = SearchWarrantyForm(request.form)
    if request.method == 'POST' and form.validate():
        warranty_product_name = request.form.get('warranty_product_name', '')
        warranties = WarrantyCard.query.filter(WarrantyCard.product_name.like(f'{warranty_product_name}%')).all()
        return render_template('warranty_mgmt/search_warranties.html', warranties=warranties, form=form)
    return render_template('warranty_mgmt/search_warranties.html', form=form)
