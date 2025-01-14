# Models/__init__.py

# Import necessary libraries
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy.event import listen
from utils.utils import delete_file

from flask_login import UserMixin


# Initialize SQLAlchemy
db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f"<Subcategory {self.name}>"


class WarrantyCard(db.Model):
    __tablename__ = 'warranty_card'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=True)  # Path to the uploaded image
    product_name= db.Column(db.String(100), nullable=False)
    warranty_number = db.Column(db.String(80), unique=True ,nullable=False)
    product_purchase_date = db.Column(db.Date(), nullable=False)
    warranty_expiry_date = db.Column(db.Date(), nullable=False)
    warranty_provider = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=True)
    # Relationships
    category = db.relationship('Category', backref='warranties')
    subcategory = db.relationship('Subcategory', backref='warranties')

def delete_image_on_warranty_delete(mapper, connection, target):
    """Delete the image file when a warranty is deleted."""
    if target.image:
        file_path = os.path.join('static', target.image)
        delete_file(file_path)

# Attach the listener to the WarrantyCard model
listen(WarrantyCard, 'before_delete', delete_image_on_warranty_delete)



class User(UserMixin, db.Model):
    """
    User model to store user data for authentication.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

