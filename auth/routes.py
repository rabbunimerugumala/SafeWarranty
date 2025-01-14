from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from schemas import RegisterUserForm, LoginForm

auth = Blueprint('auth', __name__)

# Combined Register and Login route
@auth.route('/auth', methods=['GET', 'POST'])
def auth_page():
    register_form = RegisterUserForm()
    login_form = LoginForm()

    # Handle the Register Form submission
    if request.method == 'POST' and 'sign-up' in request.form:
        # Validate passwords match
        if register_form.password.data != register_form.confirm_password.data:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.auth_page'))

        # Check if the email already exists
        existing_user = User.query.filter_by(email=register_form.email.data).first()
        if existing_user:
            flash('Email address already registered', 'danger')
            return redirect(url_for('auth.auth_page'))

        # Hash password and add user to DB
        hashed_password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256')
        new_user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.auth_page'))

    # Handle the Login Form submission
    if request.method == 'POST' and 'login' in request.form:
        user = User.query.filter_by(email=login_form.username.data).first()
        if user and check_password_hash(user.password, login_form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('warranty_mgmt.index'))
        else:
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('auth.auth_page'))

    return render_template('auth/auth_page.html', register_form=register_form, login_form=login_form)




# Logout route
@auth.route('/logout')
@login_required  # Ensure the user is logged in before they can log out
def logout():
    logout_user()  # Log out the user
    flash('You have been logged out.', 'info')  # Flash a message
    return redirect(url_for('auth.auth_page'))  # Redirect to the login page