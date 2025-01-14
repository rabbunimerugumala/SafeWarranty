# warranty_mgmt/__init__.py
from flask import Blueprint

# Initialize blueprint
warranty_mgmt = Blueprint('warranty_mgmt', __name__)

# Import routes for warranty management
from . import routes
