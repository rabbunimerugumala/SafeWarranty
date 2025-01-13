from models import db, Category, Subcategory
from main import app  # Import the app object here

with app.app_context():
    # Clear existing data from Category and Subcategory tables
    Subcategory.query.delete()  # Deletes all rows from the Subcategory table
    Category.query.delete()     # Deletes all rows from the Category table

    # Define categories and their respective subcategories
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

    # Loop through categories and subcategories to add them to the database
    for category_name, subcategories in categories.items():
        # Create and add category to the database
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()  # Commit to get the category ID

        # Loop through subcategories and add them under the created category
        for subcategory_name in subcategories:
            subcategory = Subcategory(name=subcategory_name, category_id=category.id)
            db.session.add(subcategory)

    db.session.commit()  # Commit all the subcategories after adding them
    print("Database seeded successfully!")
