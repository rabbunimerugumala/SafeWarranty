"""
This module initializes the warranty management functionality for the Flask application.

Key Features:
- Implements a Flask Blueprint for modularization and scalability.
- Encapsulates routes and logic specific to warranty management, keeping the app organized.
- Ensures warranty-related routes are grouped under the `warranty_mgmt` namespace.

Blueprint Purpose:
- A Blueprint in Flask allows you to organize your application into distinct modules.
  The `warranty_mgmt` Blueprint handles all warranty management routes, views, and related logic,
  enabling clean separation of concerns.

Dependencies:
- Flask: Used to create and manage the Blueprint.

Routes:
- The routes for warranty management are imported from the `routes` module within this package.
"""

from flask import Blueprint

# Create a Blueprint for warranty management
warranty_mgmt = Blueprint('warranty_mgmt', __name__)

# Import routes to register them with the Blueprint
from . import routes  # Ensures warranty management routes are loaded when the app starts
