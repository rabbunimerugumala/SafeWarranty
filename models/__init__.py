from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

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



