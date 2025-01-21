"""
This module initializes the 'auth' Blueprint for the Flask application.
The 'auth' Blueprint is used to define authentication-related routes
and functionalities, such as login, logout, and user registration.

By using a Blueprint, the application maintains a modular structure,
making it easier to manage and scale.
"""

from flask import Blueprint  # Importing Blueprint to create a modular route group

# Create a Blueprint for authentication-related routes
# - 'auth': The name of the Blueprint, used to reference it in the application.
# - __name__: The import name, used by Flask to locate resources like templates.
auth = Blueprint('auth', __name__)

# This file doesn't define any routes or functionality directly.
# Instead, it serves as an entry point to initialize the Blueprint
# and can be imported in other modules for route definition.
