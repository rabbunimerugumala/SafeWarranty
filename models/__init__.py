from main import db
from sqlalchemy.sql import func

# class Category(db.Model):
#     __tablename__ = 'category'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True, nullable=False)
#     subcategories = db.relationship('Subcategory', backref='category', lazy=True, cascade="all, delete-orphan")
#
# class Subcategory(db.Model):
#     __tablename__ = 'subcategory'
#     __table_args__ = {'extend_existing': True}  # Allow redefinition
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

# class Subcategory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
#     __table_args__ = (db.UniqueConstraint('name', 'category_id', name='uq_subcategory_name_category'),)


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

    # # Foreign keys
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='SET NULL'), nullable=True)
    # subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id', ondelete='SET NULL'), nullable=True)
    #
    # # Relationships
    # category = db.relationship('Category', backref='warranties')
    # subcategory = db.relationship('Subcategory', backref='warranties')




