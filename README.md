# Library Book Locator System

A Flask-based web application that helps students find the exact shelf location of books in a library using a simple search interface.

## Features

- Search for books by title, author, or ISBN
- View detailed information about each book
- See the exact shelf, column, and row location of books
- Check book availability status (Available/Issued)
- Responsive design for different screen sizes

## Technology Stack

### Backend
- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLite

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Vanilla JavaScript

## Installation and Setup

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-book-locator.git
   cd library-book-locator
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables:
   ```bash
   # For development
   export FLASK_APP=main.py
   export FLASK_ENV=development
   export SESSION_SECRET=your-secret-key
   
   # For Windows
   set FLASK_APP=main.py
   set FLASK_ENV=development
   set SESSION_SECRET=your-secret-key
   ```

5. Initialize the database:
   ```bash
   flask run
   ```
   The application will automatically create and populate the database with sample books on first run.

6. Access the application:
   Open a web browser and navigate to `http://localhost:5000`

## Database Schema

The application uses a SQLite database with the following schema:

### Book Table
- id: Primary key
- title: Book title
- author: Book author
- isbn: ISBN number (unique)
- publication_year: Year of publication
- publisher: Publisher name
- shelf: Shelf identifier (e.g., "A1", "B3")
- column: Column number on the shelf
- row: Row position (Top, Middle, Bottom)
- status: Book status (Available, Issued, Reserved, Missing)
- date_added: Date the book was added to the database
- category: Book category/genre
- description: Book description

## Deployment to Render.com

1. Create a new Web Service on Render.com
2. Connect your GitHub repository
3. Make sure to include **all** these files in your GitHub repository:
   - All Python files (app.py, main.py, models.py, etc.)
   - The `templates` and `static` directories with all their contents
   - `requirements-render.txt` file (keep this name)
   - `build.sh` script (for template directory handling)
   - `render_wsgi.py` (special file for Render deployment)
   - `render.yaml` configuration file
   - `Procfile` (for platforms that support it)
4. Configure the service on Render:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn render_wsgi:app`
5. Add the following environment variables:
   - `SESSION_SECRET`: A secure random secret key
   - `FLASK_ENV`: `production`
   - `RENDER`: `true`
   - `DATABASE_URL`: Your PostgreSQL database URL (Render provides this automatically if you add a PostgreSQL database)
6. Deploy the service

> **Important**: We updated the start command to use `render_wsgi.py` instead of `main.py`. This special file ensures that template and static files are properly handled on Render.

## Usage Guide

1. On the home page, enter a search term (book title, author, or ISBN) in the search box
2. Review the search results showing matching books
3. Click on a book to view detailed information
4. Note the shelf, column, and row information to locate the book in the library

## License

This project is licensed under the MIT License - see the LICENSE file for details.
