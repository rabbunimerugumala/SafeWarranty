"""
This script seeds the database with predefined categories and subcategories for a warranty management system.

Purpose:
- Clears any existing data in the `Category` and `Subcategory` tables.
- Populates these tables with predefined categories and their corresponding subcategories.
- Ensures a consistent and structured data hierarchy for warranties.

Dependencies:
- `models`: Contains the database models (`Category`, `Subcategory`, and `db` for database operations).
- `main`: The Flask app instance is imported to use its application context.

Usage:
- Run this script to seed the database after setting up your models and database schema.
- It is useful for initializing data in a new or reset database.
"""

from main import app  # Import the app object to use the application context
from models import db, Category, Subcategory

# Use the Flask app's application context to interact with the database
with app.app_context():
    # Clear existing data from the database tables
    Subcategory.query.delete()  # Deletes all rows from the Subcategory table
    Category.query.delete()  # Deletes all rows from the Category table

    # Define categories and their corresponding subcategories
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

    # Iterate through the dictionary to populate categories and their subcategories
    for category_name, subcategories in categories.items():
        # Create and add the category to the database
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()  # Commit to assign an ID to the category

        # Add subcategories linked to the current category
        for subcategory_name in subcategories:
            subcategory = Subcategory(name=subcategory_name, category_id=category.id)
            db.session.add(subcategory)

    # Commit all changes to the database after adding all subcategories
    db.session.commit()
    print("Database seeded successfully!")  # Print a success message
