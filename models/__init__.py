"""
This file defines the database models for the application. It uses SQLAlchemy for ORM (Object-Relational Mapping)
to handle database interactions. The models represent the schema and relationships for Categories, Subcategories,
Warranty Cards, and Users.

Key Features:
1. **Category Model**: Stores categories for the warranty system.
2. **Subcategory Model**: Represents subcategories under categories.
3. **WarrantyCard Model**: Stores detailed information about warranty cards, including image uploads, dates,
    and relationships with categories, subcategories, and users.
4. **User Model**: Stores user data for authentication and links warranties to specific users.
5. **File Deletion Listener**: Automatically deletes associated image files when a warranty card is deleted.
"""

# Import necessary libraries
import os  # For file path manipulation

from flask_login import UserMixin  # For user session management
from flask_sqlalchemy import SQLAlchemy  # For SQLAlchemy ORM
from sqlalchemy.event import listen  # For adding event listeners to models
from sqlalchemy.sql import func  # For database functions like `now()` for timestamps

from utils.utils import delete_file  # Utility function to delete files from the filesystem

# Initialize SQLAlchemy instance
db = SQLAlchemy()


# Model for storing categories
class Category(db.Model):
    """
    Represents a product category in the warranty system.
    Each category can have multiple subcategories.
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the category
    name = db.Column(db.String(100), nullable=False)  # Name of the category (e.g., Electronics, Furniture)
    subcategories = db.relationship('Subcategory', backref='category',
                                    lazy=True)  # One-to-many relationship with Subcategory

    def __repr__(self):
        return f"<Category {self.name}>"  # String representation for debugging


# Model for storing subcategories
class Subcategory(db.Model):
    """
    Represents a subcategory under a category.
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the subcategory
    name = db.Column(db.String(100), nullable=False)  # Name of the subcategory (e.g., Mobile, Laptops)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # Foreign key linking to Category

    def __repr__(self):
        return f"<Subcategory {self.name}>"  # String representation for debugging


# Model for storing warranty card information
class WarrantyCard(db.Model):
    """
    Represents a warranty card with details about the product, purchase date, and warranty expiration.
    """
    __tablename__ = 'warranty_card'  # Custom table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the warranty card
    image = db.Column(db.String(200), nullable=True)  # File path for the uploaded product image
    product_name = db.Column(db.String(100), nullable=False)  # Name of the product (e.g., Smartphone)
    warranty_number = db.Column(db.String(80), unique=True, nullable=False)  # Unique warranty number for the product
    product_purchase_date = db.Column(db.Date(), nullable=False)  # Date of purchase
    warranty_expiry_date = db.Column(db.Date(), nullable=False)  # Date of warranty expiration
    warranty_provider = db.Column(db.String(500))  # Name of the warranty provider (optional)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())  # Timestamp for creation
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())  # Timestamp for last update

    # Foreign key linking to Category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    # Foreign key linking to Subcategory
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=True)

    # Relationships
    category = db.relationship('Category', backref='warranties')  # Relationship with Category
    subcategory = db.relationship('Subcategory', backref='warranties')  # Relationship with Subcategory

    # Foreign key linking to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='user_warranties')  # Relationship with User

    def __repr__(self):
        return f"<WarrantyCard {self.product_name}>"  # String representation for debugging


# Event listener function for file deletion
def delete_image_on_warranty_delete(mapper, connection, target):
    """
    Deletes the associated image file when a warranty card is deleted.

    Args:
        mapper: SQLAlchemy mapper for the model.
        connection: Database connection object.
        target: The WarrantyCard instance being deleted.
    """
    if target.image:  # Check if there is an image file
        file_path = os.path.join('static', target.image)  # Construct the file path
        delete_file(file_path)  # Delete the file using the utility function


# Attach the listener to delete the image before a WarrantyCard is deleted
listen(WarrantyCard, 'before_delete', delete_image_on_warranty_delete)


# Model for storing user data
class User(UserMixin, db.Model):
    """
    Represents a user in the system.
    """
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    username = db.Column(db.String(20), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email address
    password = db.Column(db.String(128), nullable=False)  # Hashed password

    # Relationship with warranties: A user can have multiple warranty cards
    warranties = db.relationship('WarrantyCard', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"  # String representation for debugging
