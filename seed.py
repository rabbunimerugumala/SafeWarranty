from models import db, Category, Subcategory
from main import app  # Import the app here

with app.app_context():
    # Clear existing data
    Subcategory.query.delete()
    Category.query.delete()

    # Seed data
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

    for category_name, subcategories in categories.items():
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()  # Commit to get the category ID

        for subcategory_name in subcategories:
            subcategory = Subcategory(name=subcategory_name, category_id=category.id)
            db.session.add(subcategory)

    db.session.commit()
    print("Database seeded successfully!")
