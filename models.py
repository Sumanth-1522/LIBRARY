from app import db
from datetime import datetime

class Book(db.Model):
    """
    Book model representing a library book with location information.
    """
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
    
    # Book status
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
    
    @property
    def location_display(self):
        """Return a formatted string of the book's location."""
        return f"Shelf {self.shelf}, Column {self.column}, Row {self.row}"
    
    @property
    def status_display(self):
        """Return a human-readable status."""
        return self.STATUS_CHOICES.get(self.status, 'Unknown')
