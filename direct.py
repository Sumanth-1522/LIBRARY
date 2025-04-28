import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    A simplified Flask application for Render deployment.
    
    This uses a direct approach to create a Flask app without complexity.
    """
    # Import Flask and required dependencies
    from flask import Flask, render_template, request, redirect, url_for, flash
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy.orm import DeclarativeBase
    
    # Base class for SQLAlchemy
    class Base(DeclarativeBase):
        pass
    
    # Initialize SQLAlchemy
    db = SQLAlchemy(model_class=Base)
    
    # Create the Flask application with explicit template folder
    app = Flask(__name__)
    
    # Set up template_folder explicitly to resolve path issues
    base_dir = os.getcwd()
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')
    
    # Verify template and static directories
    logger.info(f"Base directory: {base_dir}")
    if os.environ.get('RENDER') == 'true':
        logger.info("Running on Render platform")
    else:
        logger.info("Running in local environment")
    
    logger.info(f"Setting template_folder={template_dir}, static_folder={static_dir}")
    app.template_folder = template_dir
    app.static_folder = static_dir
    
    # Log diagnostics about the template directory
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Template directory exists: {os.path.exists(template_dir)}")
    if os.path.exists(template_dir):
        logger.info(f"Template files: {os.listdir(template_dir)}")
    
    # Log application startup information
    logger.info(f"Python version: {sys.version}")
    
    # Set secret key
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
    
    # Configure database connection
    database_url = os.environ.get("DATABASE_URL", "sqlite:///library.db")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Initialize the database
    db.init_app(app)
    
    # Define embedded templates for the app (will override filesystem templates if needed)
    embedded_templates = {
        'base.html': '''<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Library Book Locator{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
    <!-- Feather Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.css">
    <!-- Custom CSS -->
    <style>
        .book-card {
            transition: transform 0.3s;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        .status-available {
            color: #28a745;
        }
        .status-issued {
            color: #dc3545;
        }
        .status-reserved {
            color: #ffc107;
        }
        .status-missing {
            color: #6c757d;
        }
        .feature-icon {
            color: var(--bs-primary);
        }
        .shelf-column {
            display: inline-block;
            position: relative;
            width: 80px;
            height: 150px;
            margin: 0 10px;
            background-color: #343a40;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        .shelf-highlight {
            background-color: rgba(0, 123, 255, 0.2);
            border-color: var(--bs-primary);
        }
        .shelf-label {
            position: absolute;
            bottom: -20px;
            width: 100%;
            text-align: center;
        }
    </style>
    {% block extra_head %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-book">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                </svg>
                Library Book Locator
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('index') }}">Home</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container my-4">
        <div id="alert-container">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>
        
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>Library Book Locator</h5>
                    <p>Find the exact shelf location of books in our library.</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p>&copy; 2023 Library Book Locator System</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Feather Icons JS -->
    <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
    <script>
        // Initialize Feather Icons
        document.addEventListener('DOMContentLoaded', function() {
            feather.replace();
        });
    </script>
    {% block extra_scripts %}{% endblock %}
</body>
</html>''',

        'index.html': '''{% extends 'base.html' %}

{% block title %}Library Book Locator - Find Your Books{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8 text-center">
        <h1 class="display-4 mb-4">Library Book Locator</h1>
        <p class="lead">Find the exact shelf location of any book in our library</p>
        
        <div class="search-container my-5">
            <form id="search-form" action="{{ url_for('search') }}" method="get">
                <div class="input-group input-group-lg">
                    <input type="text" id="search-input" name="query" class="form-control" placeholder="Search by title, author, or ISBN" aria-label="Search">
                    <button id="clear-search" type="button" class="btn btn-outline-secondary">
                        <i data-feather="x"></i>
                    </button>
                    <button id="search-button" class="btn btn-primary" type="submit">
                        <i data-feather="search"></i> Search
                    </button>
                </div>
            </form>
        </div>
        
        <div class="features mt-5">
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="card h-100 book-card">
                        <div class="card-body text-center">
                            <div class="feature-icon mb-3">
                                <i data-feather="map-pin" style="width: 48px; height: 48px;"></i>
                            </div>
                            <h5 class="card-title">Precise Location</h5>
                            <p class="card-text">Find the exact shelf, column, and row for any book</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100 book-card">
                        <div class="card-body text-center">
                            <div class="feature-icon mb-3">
                                <i data-feather="check-circle" style="width: 48px; height: 48px;"></i>
                            </div>
                            <h5 class="card-title">Availability Status</h5>
                            <p class="card-text">Check if a book is available or currently issued</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100 book-card">
                        <div class="card-body text-center">
                            <div class="feature-icon mb-3">
                                <i data-feather="info" style="width: 48px; height: 48px;"></i>
                            </div>
                            <h5 class="card-title">Book Details</h5>
                            <p class="card-text">View complete information about each book</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="how-to-use mt-5">
            <h2 class="mb-4">How to Use</h2>
            <div class="card">
                <div class="card-body">
                    <ol class="text-start">
                        <li>Enter the title, author, or ISBN of the book you're looking for in the search box above.</li>
                        <li>Click the "Search" button or press Enter to see results.</li>
                        <li>Browse through the search results to find your book.</li>
                        <li>Click on any book to see detailed information, including its exact location in the library.</li>
                        <li>Use the shelf, column, and row information to locate your book.</li>
                    </ol>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

        'search_results.html': '''{% extends 'base.html' %}

{% block title %}Search Results for "{{ query }}" - Library Book Locator{% endblock %}

{% block content %}
<div class="container">
    <div class="row mb-4">
        <div class="col-12">
            <h1>Search Results</h1>
            <p class="lead">Found {{ books|length }} result(s) for "{{ query }}"</p>
            
            <!-- Quick search form -->
            <form id="search-form" action="{{ url_for('search') }}" method="get" class="mb-4">
                <div class="input-group">
                    <input type="text" id="search-input" name="query" class="form-control" placeholder="Search by title, author, or ISBN" value="{{ query }}" aria-label="Search">
                    <button id="clear-search" type="button" class="btn btn-outline-secondary">
                        <i data-feather="x"></i>
                    </button>
                    <button id="search-button" class="btn btn-primary" type="submit">
                        <i data-feather="search"></i> Search
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    {% if books %}
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            {% for book in books %}
                <div class="col">
                    <div class="card h-100 book-card">
                        <div class="card-body">
                            <h5 class="card-title">{{ book.title }}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
                            
                            <div class="mt-3">
                                <span class="badge bg-{{ 'success' if book.status == 'available' else 'danger' if book.status == 'issued' else 'warning' if book.status == 'reserved' else 'secondary' }} status-badge status-{{ book.status }}">
                                    {{ book.status_display() }}
                                </span>
                            </div>
                            
                            <p class="card-text mt-3">
                                <strong>Location:</strong> {{ book.location_display() }}
                            </p>
                            
                            <p class="card-text">
                                <small class="text-muted">ISBN: {{ book.isbn }}</small>
                            </p>
                        </div>
                        <div class="card-footer">
                            <a href="{{ url_for('book_details', book_id=book.id) }}" class="btn btn-outline-primary btn-sm">View Details</a>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-info" role="alert">
            <h4 class="alert-heading">No books found!</h4>
            <p>We couldn't find any books matching your search criteria. Please try a different search term.</p>
            <hr>
            <p class="mb-0">Try searching for a book title, author name, or ISBN.</p>
        </div>
        
        <div class="text-center mt-4">
            <a href="{{ url_for('index') }}" class="btn btn-primary">
                <i data-feather="arrow-left"></i> Back to Home
            </a>
        </div>
    {% endif %}
</div>
{% endblock %}''',

        'book_details.html': '''{% extends 'base.html' %}

{% block title %}{{ book.title }} - Library Book Locator{% endblock %}

{% block content %}
<div class="container book-details">
    <div class="row">
        <div class="col-12 mb-4">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{{ url_for('index') }}">Home</a></li>
                    <li class="breadcrumb-item"><a href="{{ url_for('search', query=book.title) }}">Search Results</a></li>
                    <li class="breadcrumb-item active" aria-current="page">Book Details</li>
                </ol>
            </nav>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-8">
            <h1 class="book-title">{{ book.title }}</h1>
            <p class="book-author">by {{ book.author }}</p>
            
            <div class="mb-4">
                <span class="badge bg-{{ 'success' if book.status == 'available' else 'danger' if book.status == 'issued' else 'warning' if book.status == 'reserved' else 'secondary' }} status-badge status-{{ book.status }}">
                    {{ book.status_display() }}
                </span>
                <span class="badge bg-secondary ms-2">{{ book.category }}</span>
            </div>
            
            {% if book.description %}
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">Description</h5>
                        <p class="card-text">{{ book.description }}</p>
                    </div>
                </div>
            {% endif %}
            
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">Book Details</h5>
                    <table class="table table-striped">
                        <tbody>
                            <tr>
                                <th scope="row">ISBN</th>
                                <td>{{ book.isbn }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Publication Year</th>
                                <td>{{ book.publication_year }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Publisher</th>
                                <td>{{ book.publisher }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Category</th>
                                <td>{{ book.category }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Status</th>
                                <td>
                                    <span class="status-{{ book.status }}">{{ book.status_display() }}</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="card-title mb-0">
                        <i data-feather="map-pin" class="me-2"></i> Book Location
                    </h5>
                </div>
                <div class="card-body" id="book-location" data-shelf="{{ book.shelf }}" data-column="{{ book.column }}" data-row="{{ book.row }}">
                    <div class="d-flex align-items-center mb-4">
                        <div class="location-icon me-3">
                            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-book-open">
                                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                            </svg>
                        </div>
                        <div>
                            <h4 class="mb-0">{{ book.location_display() }}</h4>
                        </div>
                    </div>
                    
                    <div class="location-details">
                        <div class="d-flex justify-content-between mb-2">
                            <span><strong>Shelf:</strong></span>
                            <span class="badge bg-primary">{{ book.shelf }}</span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span><strong>Column:</strong></span>
                            <span class="badge bg-info">{{ book.column }}</span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span><strong>Row:</strong></span>
                            <span class="badge bg-secondary">{{ book.row }}</span>
                        </div>
                    </div>
                    
                    <div class="shelf-map mt-4">
                        <h6 class="text-center mb-3">Shelf Visualization</h6>
                        <div class="text-center">
                            <!-- Simple visual representation of the shelf -->
                            {% for col in range(1, 4) %}
                                <div class="shelf-column {{ 'shelf-highlight' if book.column == col|string }}">
                                    <div style="position: absolute; top: {{ 25 if book.row == 'Top' else 50 if book.row == 'Middle' else 75 }}%; left: 0; right: 0; text-align: center;">
                                        {% if book.column == col|string and book.shelf == book.shelf %}
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-book">
                                                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                                                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                                            </svg>
                                        {% endif %}
                                    </div>
                                    <div class="shelf-label">{{ col }}</div>
                                </div>
                            {% endfor %}
                            <div class="mt-4">
                                <small class="text-muted">Shelf {{ book.shelf }}</small>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{{ url_for('index') }}" class="btn btn-outline-secondary btn-sm">
                        <i data-feather="arrow-left"></i> Back to Search
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

        'error.html': '''{% extends 'base.html' %}

{% block title %}Error - Library Book Locator{% endblock %}

{% block content %}
<div class="container text-center">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="error-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-alert-circle mb-4">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                
                <h1 class="display-1 mb-4">{{ error|default('Error') }}</h1>
                
                <p class="lead">{{ message|default('Something went wrong. Please try again later.') }}</p>
                
                <div class="mt-5">
                    <a href="{{ url_for('index') }}" class="btn btn-primary btn-lg">
                        <i data-feather="home"></i> Return to Home Page
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    }
    
    # Create a custom template loader for embedded templates
    try:
        from jinja2 import DictLoader, ChoiceLoader, FileSystemLoader
        app.jinja_loader = ChoiceLoader([
            DictLoader(embedded_templates),
            FileSystemLoader(template_dir)
        ])
        logger.info("Successfully set up custom template loader")
    except Exception as e:
        logger.error(f"Error setting up custom template loader: {e}")
        # If the custom loader fails, fall back to embedded templates only
        from jinja2 import DictLoader
        app.jinja_loader = DictLoader(embedded_templates)
        logger.info("Falling back to embedded templates only")
    
    # Import models and create tables
    with app.app_context():
        # Define Book model
        class Book(db.Model):
            """Book model representing a library book with location information."""
            id = db.Column(db.Integer, primary_key=True)
            title = db.Column(db.String(200), nullable=False)
            author = db.Column(db.String(100), nullable=False)
            isbn = db.Column(db.String(20), unique=True, nullable=False)
            publication_year = db.Column(db.Integer)
            publisher = db.Column(db.String(100))
            
            # Location information
            shelf = db.Column(db.String(10), nullable=False)  # e.g., "A1", "B3"
            column = db.Column(db.String(10), nullable=False)  # e.g., "1", "2", "3"
            row = db.Column(db.String(10), nullable=False)    # e.g., "Top", "Middle", "Bottom"
            
            # Status information
            STATUS_CHOICES = {
                'available': 'Available',
                'issued': 'Issued',
                'reserved': 'Reserved',
                'missing': 'Missing'
            }
            
            status = db.Column(db.String(20), default='available')
            date_added = db.Column(db.DateTime, default=datetime.utcnow)
            category = db.Column(db.String(50))
            description = db.Column(db.Text)
            
            def __repr__(self):
                return f"<Book {self.title} by {self.author}>"
            
            def location_display(self):
                """Return a formatted string of the book's location."""
                return f"Shelf {self.shelf}, Column {self.column}, Row {self.row}"
            
            def status_display(self):
                """Return a human-readable status."""
                return self.STATUS_CHOICES.get(self.status, self.status)
                
        # Create all tables
        db.create_all()
        
        # Seed database if empty
        if Book.query.count() == 0:
            logger.info("Seeding database with initial data...")
            
            books = [
                Book(
                    title="Python Crash Course",
                    author="Eric Matthes",
                    isbn="9781593279288",
                    publication_year=2019,
                    publisher="No Starch Press",
                    shelf="A1",
                    column="1",
                    row="Top",
                    status="available",
                    category="Programming",
                    description="A hands-on, project-based introduction to programming."
                ),
                Book(
                    title="The Great Gatsby",
                    author="F. Scott Fitzgerald",
                    isbn="9780743273565",
                    publication_year=1925,
                    publisher="Scribner",
                    shelf="B2",
                    column="3",
                    row="Middle",
                    status="available",
                    category="Fiction",
                    description="A novel about the American Dream set in the Jazz Age."
                ),
                Book(
                    title="To Kill a Mockingbird",
                    author="Harper Lee",
                    isbn="9780061120084",
                    publication_year=1960,
                    publisher="HarperCollins",
                    shelf="B3",
                    column="2",
                    row="Bottom",
                    status="issued",
                    category="Fiction",
                    description="A novel about racial injustice in the American South."
                ),
                Book(
                    title="Database Systems: The Complete Book",
                    author="Hector Garcia-Molina",
                    isbn="9780131873254",
                    publication_year=2008,
                    publisher="Pearson",
                    shelf="C1",
                    column="4",
                    row="Top",
                    status="available",
                    category="Computer Science",
                    description="A comprehensive introduction to database systems."
                ),
                Book(
                    title="Algorithms to Live By",
                    author="Brian Christian",
                    isbn="9781627790369",
                    publication_year=2016,
                    publisher="Henry Holt & Co.",
                    shelf="A2",
                    column="2",
                    row="Middle",
                    status="reserved",
                    category="Science",
                    description="How computer algorithms can be applied to human decisions."
                ),
                Book(
                    title="Pride and Prejudice",
                    author="Jane Austen",
                    isbn="9780141439518",
                    publication_year=1813,
                    publisher="Penguin Classics",
                    shelf="B1",
                    column="1",
                    row="Bottom",
                    status="available",
                    category="Fiction",
                    description="A romantic novel of manners in early 19th century England."
                ),
                Book(
                    title="Machine Learning: A Probabilistic Perspective",
                    author="Kevin P. Murphy",
                    isbn="9780262018029",
                    publication_year=2012,
                    publisher="MIT Press",
                    shelf="D2",
                    column="3",
                    row="Top",
                    status="available",
                    category="Computer Science",
                    description="A comprehensive introduction to machine learning algorithms."
                ),
                Book(
                    title="The Art of Computer Programming",
                    author="Donald E. Knuth",
                    isbn="9780201896831",
                    publication_year=1968,
                    publisher="Addison-Wesley",
                    shelf="D1",
                    column="5",
                    row="Middle",
                    status="available",
                    category="Computer Science",
                    description="A comprehensive monograph on computer programming techniques."
                ),
                Book(
                    title="Sapiens: A Brief History of Humankind",
                    author="Yuval Noah Harari",
                    isbn="9780062316097",
                    publication_year=2014,
                    publisher="Harper",
                    shelf="E3",
                    column="2",
                    row="Top",
                    status="available",
                    category="History",
                    description="A brief overview of human evolutionary history."
                ),
                Book(
                    title="The Hitchhiker's Guide to the Galaxy",
                    author="Douglas Adams",
                    isbn="9780345391803",
                    publication_year=1979,
                    publisher="Del Rey",
                    shelf="F2",
                    column="1",
                    row="Bottom",
                    status="missing",
                    category="Science Fiction",
                    description="A comedic science fiction series created by Douglas Adams."
                )
            ]
            
            for book in books:
                db.session.add(book)
            
            db.session.commit()
            logger.info("Database seeded successfully.")
    
    # Define routes with error handling
    @app.route('/')
    def index():
        """Render the main page with search functionality."""
        try:
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error rendering index template: {e}")
            # Provide a fallback homepage if template fails
            return """
            <!DOCTYPE html>
            <html lang="en" data-bs-theme="dark">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Library Book Locator</title>
                <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
            </head>
            <body>
                <div class="container text-center py-5">
                    <h1 class="display-4 mb-4">Library Book Locator</h1>
                    <p class="lead">Find the exact shelf location of any book in our library</p>
                    
                    <div class="mt-5">
                        <form action="/search" method="get" class="mb-4">
                            <div class="input-group input-group-lg mb-3">
                                <input type="text" name="query" class="form-control" placeholder="Search by title, author, or ISBN">
                                <button class="btn btn-primary" type="submit">Search</button>
                            </div>
                        </form>
                    </div>
                    
                    <div class="row g-4 mt-4">
                        <div class="col-md-4">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Precise Location</h5>
                                    <p class="card-text">Find the exact shelf, column, and row for any book</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Availability Status</h5>
                                    <p class="card-text">Check if a book is available or currently issued</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card h-100">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Book Details</h5>
                                    <p class="card-text">View complete information about each book</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
    
    @app.route('/search', methods=['GET', 'POST'])
    def search():
        """Handle search requests and display results."""
        search_query = request.args.get('query', '') if request.method == 'GET' else request.form.get('query', '')
        
        if not search_query:
            flash('Please enter a search term.', 'warning')
            return redirect(url_for('index'))
        
        # Search for books by title, author, or ISBN
        books = Book.query.filter(
            (Book.title.ilike(f'%{search_query}%')) | 
            (Book.author.ilike(f'%{search_query}%')) | 
            (Book.isbn.ilike(f'%{search_query}%'))
        ).all()
        
        try:
            return render_template('search_results.html', books=books, query=search_query)
        except Exception as e:
            logger.error(f"Error rendering search results template: {e}")
            # Fallback search results
            html = """
            <!DOCTYPE html>
            <html lang="en" data-bs-theme="dark">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Search Results - Library Book Locator</title>
                <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
            </head>
            <body>
                <div class="container py-5">
                    <h1>Search Results</h1>
                    <p class="lead">Results for "{{query}}"</p>
                    
                    <div class="mb-4">
                        <a href="/" class="btn btn-outline-secondary">Back to Home</a>
                    </div>
            """
            
            if books:
                html += "<div class='row row-cols-1 row-cols-md-3 g-4'>"
                for book in books:
                    status_class = "success" if book.status == "available" else "danger" if book.status == "issued" else "warning"
                    html += f"""
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">{book.title}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">{book.author}</h6>
                                <p class="card-text">
                                    <strong>Location:</strong> {book.location_display()}<br>
                                    <strong>Status:</strong> <span class="badge bg-{status_class}">{book.status_display()}</span><br>
                                    <small>ISBN: {book.isbn}</small>
                                </p>
                            </div>
                            <div class="card-footer">
                                <a href="/book/{book.id}" class="btn btn-outline-primary btn-sm">View Details</a>
                            </div>
                        </div>
                    </div>
                    """
                html += "</div>"
            else:
                html += """
                <div class="alert alert-info" role="alert">
                    <h4 class="alert-heading">No books found!</h4>
                    <p>We couldn't find any books matching your search criteria. Please try a different search term.</p>
                </div>
                """
            
            html += """
                </div>
            </body>
            </html>
            """
            
            return html.replace("{{query}}", search_query)
    
    @app.route('/book/<int:book_id>')
    def book_details(book_id):
        """Display detailed information about a specific book."""
        try:
            book = Book.query.get_or_404(book_id)
            return render_template('book_details.html', book=book)
        except Exception as e:
            logger.error(f"Error rendering book details template: {e}")
            # Try to get the book
            book = None
            try:
                book = Book.query.get(book_id)
            except Exception as db_error:
                logger.error(f"Error retrieving book from database: {db_error}")
                return redirect(url_for('index'))
                
            if not book:
                return redirect(url_for('index'))
                
            # Fallback book details page
            status_class = "success" if book.status == "available" else "danger" if book.status == "issued" else "warning"
            return f"""
            <!DOCTYPE html>
            <html lang="en" data-bs-theme="dark">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{book.title} - Library Book Locator</title>
                <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
            </head>
            <body>
                <div class="container py-5">
                    <nav aria-label="breadcrumb">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item"><a href="/">Home</a></li>
                            <li class="breadcrumb-item active" aria-current="page">Book Details</li>
                        </ol>
                    </nav>
                    
                    <div class="row">
                        <div class="col-md-8">
                            <h1>{book.title}</h1>
                            <p class="lead">by {book.author}</p>
                            
                            <div class="mb-4">
                                <span class="badge bg-{status_class}">{book.status_display()}</span>
                                <span class="badge bg-secondary ms-2">{book.category}</span>
                            </div>
                            
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h5 class="card-title">Description</h5>
                                    <p class="card-text">{book.description}</p>
                                </div>
                            </div>
                            
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h5 class="card-title">Book Details</h5>
                                    <table class="table">
                                        <tbody>
                                            <tr>
                                                <th>ISBN</th>
                                                <td>{book.isbn}</td>
                                            </tr>
                                            <tr>
                                                <th>Publication Year</th>
                                                <td>{book.publication_year}</td>
                                            </tr>
                                            <tr>
                                                <th>Publisher</th>
                                                <td>{book.publisher}</td>
                                            </tr>
                                            <tr>
                                                <th>Status</th>
                                                <td>{book.status_display()}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-header bg-primary text-white">
                                    <h5 class="card-title mb-0">Book Location</h5>
                                </div>
                                <div class="card-body">
                                    <h4 class="mb-3">{book.location_display()}</h4>
                                    
                                    <div class="d-flex justify-content-between mb-2">
                                        <span><strong>Shelf:</strong></span>
                                        <span class="badge bg-primary">{book.shelf}</span>
                                    </div>
                                    <div class="d-flex justify-content-between mb-2">
                                        <span><strong>Column:</strong></span>
                                        <span class="badge bg-info">{book.column}</span>
                                    </div>
                                    <div class="d-flex justify-content-between mb-2">
                                        <span><strong>Row:</strong></span>
                                        <span class="badge bg-secondary">{book.row}</span>
                                    </div>
                                </div>
                                <div class="card-footer">
                                    <a href="/" class="btn btn-outline-secondary btn-sm">Back to Home</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
    
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors."""
        try:
            return render_template('error.html', error="Page not found"), 404
        except Exception as template_error:
            # Fallback error response if template is unavailable
            logger.error(f"Could not render error template: {template_error}")
            return """
            <!DOCTYPE html>
            <html lang="en" data-bs-theme="dark">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Page Not Found - Library Book Locator</title>
                <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
            </head>
            <body>
                <div class="container text-center py-5">
                    <h1 class="display-1">404</h1>
                    <h2>Page Not Found</h2>
                    <p class="lead">The page you were looking for does not exist.</p>
                    <a href="/" class="btn btn-primary mt-3">Return to Home</a>
                </div>
            </body>
            </html>
            """, 404
    
    @app.errorhandler(500)
    def server_error(e):
        """Handle 500 errors."""
        try:
            return render_template('error.html', error="Internal server error"), 500
        except Exception as template_error:
            # Fallback error response if template is unavailable
            logger.error(f"Could not render error template: {template_error}")
            return """
            <!DOCTYPE html>
            <html lang="en" data-bs-theme="dark">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Server Error - Library Book Locator</title>
                <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
            </head>
            <body>
                <div class="container text-center py-5">
                    <h1 class="display-1">500</h1>
                    <h2>Internal Server Error</h2>
                    <p class="lead">Something went wrong on our end. Please try again later.</p>
                    <a href="/" class="btn btn-primary mt-3">Return to Home</a>
                </div>
            </body>
            </html>
            """, 500
    
    # Return the app for gunicorn
    return app

# Create the application instance for gunicorn
app = main()

if __name__ == "__main__":
    # Run the app directly when executed as a script
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)