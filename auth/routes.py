from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from schemas import RegisterUserForm, LoginForm

auth = Blueprint('auth', __name__)

# Register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        # Check if the user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address already registered', 'danger')
            return redirect(url_for('auth.register'))

        # Create a new user and hash the password
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


# Login route
# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Fetch all users from the database to check if the email exists
        users = User.query.all()  # Fetches all users
        for user in users:
            print(f"User in DB: {user.email}, {user.username}")  # Print out the emails and usernames of all users

        user = User.query.filter_by(email=form.username.data).first()
        if user:
            print(f"User found: {user.email}")
        else:
            print("User not found.")
            flash('User not found.', 'danger')
            return redirect(url_for('auth.login'))

        if check_password_hash(user.password, form.password.data):
            login_user(user)
            print(f"Logged in user: {user.email}")
            flash('Login successful!', 'success')
            return redirect(url_for('warranty_mgmt.index'))
        else:
            print("Invalid password.")
            flash('Invalid password.', 'danger')

    return render_template('auth/login.html', form=form)



# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))  # Redirect to login after logout
