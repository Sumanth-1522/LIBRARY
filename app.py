import os
import logging
import sys
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the base class
db = SQLAlchemy(model_class=Base)

# Get the directory where app.py is located
BASE_DIR = Path(__file__).resolve().parent
logger.info(f"Base directory: {BASE_DIR}")

# CRITICAL: Handle templates explicitly for Render deployment
if os.environ.get('RENDER'):
    logger.info("Running in Render environment, using pre-copied template files")
    template_dir = os.path.join("/opt/render/project/src", "templates")
    static_dir = os.path.join("/opt/render/project/src", "static")
else:
    logger.info("Running in local environment")
    template_dir = os.path.join(BASE_DIR, "templates")
    static_dir = os.path.join(BASE_DIR, "static")

# Log the directories to help with debugging
logger.info(f"Template directory exists: {os.path.exists(template_dir)}")
if os.path.exists(template_dir):
    template_files = os.listdir(template_dir)
    logger.info(f"Template files: {template_files}")
else:
    logger.error(f"Template directory NOT FOUND: {template_dir}")

# Create the Flask application with explicit template folder
app = Flask(__name__, 
            template_folder=template_dir,
            static_folder=static_dir)

# Log important paths to help with debugging
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Template directory: {template_dir}")
logger.info(f"Static directory: {static_dir}")

app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure database connection
database_url = os.environ.get("DATABASE_URL", "sqlite:///library.db")
# Fix for PostgreSQL URL format for Render deployment
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the application with Flask-SQLAlchemy
db.init_app(app)

# Import routes and models after initializing db to avoid circular imports
with app.app_context():
    # Import models
    from models import Book
    
    # Create all database tables
    db.create_all()
    
    # Check if the database needs to be seeded with initial data
    if Book.query.count() == 0:
        from seed_data import seed_database
        seed_database()
        app.logger.info("Database seeded with initial book data.")

# Routes
@app.route('/')
def index():
    """Render the main page with search functionality."""
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle search requests and display results."""
    search_query = request.args.get('query', '') if request.method == 'GET' else request.form.get('query', '')
    
    if not search_query:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('index'))
    
    # Search for books by title, author, or ISBN
    from models import Book
    books = Book.query.filter(
        (Book.title.ilike(f'%{search_query}%')) | 
        (Book.author.ilike(f'%{search_query}%')) | 
        (Book.isbn.ilike(f'%{search_query}%'))
    ).all()
    
    return render_template('search_results.html', books=books, query=search_query)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    """Display detailed information about a specific book."""
    from models import Book
    book = Book.query.get_or_404(book_id)
    return render_template('book_details.html', book=book)

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template('error.html', error="Internal server error"), 500

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
