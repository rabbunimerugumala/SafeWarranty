from flask import Flask, redirect, url_for, render_template, flash
from models import db, User
from auth.routes import auth
from warranty_mgmt.routes import warranty_mgmt
from flask_login import LoginManager, login_user, login_required, current_user
import os

app = Flask(__name__)

# Secret key for sessions
app.secret_key = os.urandom(24)  # You can also use a fixed secret key in production

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))  # Get the base directory of the app
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'db', 'database.db')}"  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db.init_app(app)  # Initialize the database

# Flask-Login Initialization
login_manager = LoginManager()
login_manager.init_app(app)

# Ensure login view is set for unauthorized access
login_manager.login_view = 'auth.auth_page'  # Redirect to login if unauthorized
login_manager.login_message_category = 'danger'  # Customize flash message category for login

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')  # All auth-related routes start with '/auth'
app.register_blueprint(warranty_mgmt, url_prefix='/warranty')  # All warranty-related routes start with '/warranty'

# Home route - redirects to login if user is not authenticated
@app.route('/')
def home():
    if current_user.is_authenticated:  # Check if the user is authenticated
        return redirect(url_for('warranty_mgmt.index'))  # Redirect to warranty_mgmt.index if logged in
    return redirect(url_for('auth.auth_page'))  # Otherwise, redirect to login page

# Load user by ID (required for Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Cleanup database session after request
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# Run the application
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
