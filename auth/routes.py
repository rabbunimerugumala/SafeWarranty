"""
This module handles user authentication for the Flask application. 
It provides routes for user registration, login, and logout functionality, 
along with form validation and password security. 

Key features:
- Combined route for user registration and login for simplicity.
- Password hashing for secure storage using Werkzeug.
- Flask-Login integration for session management.

Dependencies:
- Flask-Login: Manages user session state.
- Werkzeug: Provides secure password hashing.
- Custom models (`User`, `db`) and forms (`RegisterUserForm`, `LoginForm`).

Routes:
1. `/auth` - Combined registration and login page.
2. `/logout` - Logs out the user.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, db  # Import User model and database instance
from schemas import RegisterUserForm, LoginForm  # Import form schemas for validation

# Create a Blueprint for authentication-related routes
auth = Blueprint('auth', __name__)


# Combined Register and Login route
@auth.route('/auth', methods=['GET', 'POST'])
def auth_page():
    """
    Handles both user registration and login on a single page.

    Methods:
    - GET: Renders the registration and login forms.
    - POST: Processes form submissions (either 'sign-up' or 'login').
    """
    # Create instances of the registration and login forms
    register_form = RegisterUserForm()
    login_form = LoginForm()

    # Handle the Register Form submission
    if request.method == 'POST' and 'sign-up' in request.form:
        # Ensure passwords match
        if register_form.password.data != register_form.confirm_password.data:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.auth_page'))

        # Check if the email is already registered
        existing_user = User.query.filter_by(email=register_form.email.data).first()
        if existing_user:
            flash('Email address already registered', 'danger')
            return redirect(url_for('auth.auth_page'))

        # Hash the password for security and create a new user
        hashed_password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256')
        new_user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)  # Add the new user to the database
        db.session.commit()  # Save changes to the database

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.auth_page'))

    # Handle the Login Form submission
    if request.method == 'POST' and 'login' in request.form:
        # Retrieve the user by email
        user = User.query.filter_by(email=login_form.username.data).first()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, login_form.password.data):
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('warranty_mgmt.index'))  # Redirect to the dashboard
        else:
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('auth.auth_page'))

    # Render the combined registration and login page with both forms
    return render_template('auth/auth_page.html', register_form=register_form, login_form=login_form)


# Logout route
@auth.route('/logout')
@login_required  # Ensure the user is logged in before they can log out
def logout():
    """
    Logs out the current user and redirects to the login page.
    """
    logout_user()  # Terminate the user's session
    flash('You have been logged out.', 'info')  # Display a logout message
    return redirect(url_for('auth.auth_page'))  # Redirect to the combined auth page
