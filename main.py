"""
Warranty Management System - Flask Application
Author: MERUGUMALA RABBUNI
Version: 1.0

Description:
This is the main application file for the Warranty Management System, designed to manage user authentication, warranty information, and related functionalities. The project uses Flask as the web framework, SQLAlchemy for database interaction, and Flask-Login for user session management.

Key Features:
1. Modular Design: Organizes routes using Blueprints (`auth` for authentication and `warranty_mgmt` for warranty-related features).
2. Database Integration: Utilizes SQLite with SQLAlchemy ORM for seamless database interaction.
3. User Authentication: Manages user login, logout, and session handling with Flask-Login.
4. Extensibility: Built with scalability in mind, making it easy to add more features in the future.
5. Database Migrations: Integrated Flask-Migrate to manage database schema changes.

Usage:
Run this file to start the application:
    python main.py

This file demonstrates:
- Flask app initialization
- Database and migration setup
- Blueprint registration
- User session and authentication handling
"""

import os

from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate  # For handling database migrations

from auth.routes import auth
from models import db, User
from warranty_mgmt.routes import warranty_mgmt

app = Flask(__name__)

# ! 1. Configure the app
# Secret key for secure sessions
app.secret_key = os.urandom(24)  # Random secret key for sessions (use a fixed key in production)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))  # Base directory of the app
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'db', 'database.db')}"  # SQLite database path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for better performance

# ! 2. Initialize database and migration tools
db.init_app(app)  # Link SQLAlchemy to the app
migrate = Migrate(app, db)  # Setup Flask-Migrate for database migrations

# ! 3. Set up Flask-Login
login_manager = LoginManager()  # Create a login manager instance
login_manager.init_app(app)  # Initialize the login manager
login_manager.login_view = 'auth.auth_page'  # Redirect to login page for unauthorized access
login_manager.login_message_category = 'danger'  # Flash category for login messages

# ! 4. Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')  # Routes for user authentication (e.g., login, register)
app.register_blueprint(warranty_mgmt, url_prefix='/warranty')  # Routes for warranty management


# ! 5. Define application routes
# Home route
@app.route('/')
def home():
    """
    Redirects users based on authentication status:
    - If logged in: Redirect to the warranty management index page.
    - If not logged in: Redirect to the login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('warranty_mgmt.index'))  # Redirect to warranty management system
    return redirect(url_for('auth.auth_page'))  # Redirect to login page


# Flask-Login: Load user by ID
@login_manager.user_loader
def load_user(user_id):
    """
    Fetches the user from the database based on their ID.
    This is required by Flask-Login to manage user sessions.
    """
    return User.query.get(int(user_id))  # Retrieve the user by their unique ID


# Cleanup database session after each request
@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Ensures the database session is removed after every request.
    This prevents issues like connection leakage.
    """
    db.session.remove()


# ! 6. Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Start the app with debugging enabled
