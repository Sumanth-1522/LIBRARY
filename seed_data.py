"""
This module contains functions to seed the database with initial data.
"""
from app import db
from models import Book

def seed_database():
    """
    Seed the database with a collection of sample books.
    """
    books = [
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'isbn': '9780061120084',
            'publication_year': 1960,
            'publisher': 'HarperCollins',
            'shelf': 'A1',
            'column': '1',
            'row': 'Middle',
            'status': 'available',
            'category': 'Fiction',
            'description': 'The unforgettable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it.'
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'isbn': '9780451524935',
            'publication_year': 1949,
            'publisher': 'Signet Classic',
            'shelf': 'A1',
            'column': '2',
            'row': 'Top',
            'status': 'available',
            'category': 'Fiction',
            'description': 'Among the seminal texts of the 20th century, Nineteen Eighty-Four is a rare work that grows more haunting as its futuristic purgatory becomes more real.'
        },
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'isbn': '9780743273565',
            'publication_year': 1925,
            'publisher': 'Scribner',
            'shelf': 'A1',
            'column': '3',
            'row': 'Bottom',
            'status': 'issued',
            'category': 'Fiction',
            'description': 'A true classic of twentieth-century literature.'
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'isbn': '9780141439518',
            'publication_year': 1813,
            'publisher': 'Penguin Classics',
            'shelf': 'A2',
            'column': '1',
            'row': 'Middle',
            'status': 'available',
            'category': 'Fiction',
            'description': 'Few have failed to be charmed by the witty and independent spirit of Elizabeth Bennet.'
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'isbn': '9780547928227',
            'publication_year': 1937,
            'publisher': 'Houghton Mifflin Harcourt',
            'shelf': 'A2',
            'column': '2',
            'row': 'Top',
            'status': 'available',
            'category': 'Fantasy',
            'description': 'A glorious account of a magnificent adventure, filled with suspense and seasoned with a quiet humor.'
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'isbn': '9780316769488',
            'publication_year': 1951,
            'publisher': 'Little, Brown and Company',
            'shelf': 'A2',
            'column': '3',
            'row': 'Bottom',
            'status': 'available',
            'category': 'Fiction',
            'description': 'The hero-narrator of The Catcher in the Rye is an ancient child of sixteen, a native New Yorker named Holden Caulfield.'
        },
        {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'isbn': '9780618640157',
            'publication_year': 1954,
            'publisher': 'Houghton Mifflin Harcourt',
            'shelf': 'B1',
            'column': '1',
            'row': 'Top',
            'status': 'available',
            'category': 'Fantasy',
            'description': 'An epic adventure of good against evil, a quest to destroy a dangerous magical object: the Ring.'
        },
        {
            'title': 'Brave New World',
            'author': 'Aldous Huxley',
            'isbn': '9780060850524',
            'publication_year': 1932,
            'publisher': 'Harper Perennial',
            'shelf': 'B1',
            'column': '2',
            'row': 'Middle',
            'status': 'issued',
            'category': 'Fiction',
            'description': 'Aldous Huxley\'s profoundly important classic of world literature.'
        },
        {
            'title': 'The Alchemist',
            'author': 'Paulo Coelho',
            'isbn': '9780061122415',
            'publication_year': 1988,
            'publisher': 'HarperOne',
            'shelf': 'B1',
            'column': '3',
            'row': 'Bottom',
            'status': 'available',
            'category': 'Fiction',
            'description': 'This story, dazzling in its powerful simplicity and soul-stirring wisdom, is about an Andalusian shepherd boy.'
        },
        {
            'title': 'Animal Farm',
            'author': 'George Orwell',
            'isbn': '9780451526342',
            'publication_year': 1945,
            'publisher': 'Signet Classics',
            'shelf': 'B2',
            'column': '1',
            'row': 'Top',
            'status': 'available',
            'category': 'Fiction',
            'description': 'A farm is taken over by its overworked, mistreated animals.'
        },
        {
            'title': 'The Odyssey',
            'author': 'Homer',
            'isbn': '9780143039952',
            'publication_year': -800,
            'publisher': 'Penguin Classics',
            'shelf': 'B2',
            'column': '2',
            'row': 'Middle',
            'status': 'available',
            'category': 'Classics',
            'description': 'The epic tale of Odysseus\'s journey home after the Trojan War.'
        },
        {
            'title': 'Moby-Dick',
            'author': 'Herman Melville',
            'isbn': '9780142437247',
            'publication_year': 1851,
            'publisher': 'Penguin Classics',
            'shelf': 'B2',
            'column': '3',
            'row': 'Bottom',
            'status': 'available',
            'category': 'Fiction',
            'description': 'The saga of Captain Ahab and his obsession with the white whale.'
        },
        {
            'title': 'Jane Eyre',
            'author': 'Charlotte Brontë',
            'isbn': '9780141441146',
            'publication_year': 1847,
            'publisher': 'Penguin Classics',
            'shelf': 'C1',
            'column': '1',
            'row': 'Top',
            'status': 'issued',
            'category': 'Fiction',
            'description': 'The story of a passionate young woman who follows her heart.'
        },
        {
            'title': 'Frankenstein',
            'author': 'Mary Shelley',
            'isbn': '9780141439471',
            'publication_year': 1818,
            'publisher': 'Penguin Classics',
            'shelf': 'C1',
            'column': '2',
            'row': 'Middle',
            'status': 'available',
            'category': 'Fiction',
            'description': 'The chilling tale of Victor Frankenstein and his creation.'
        },
        {
            'title': 'The Divine Comedy',
            'author': 'Dante Alighieri',
            'isbn': '9780142437223',
            'publication_year': 1320,
            'publisher': 'Penguin Classics',
            'shelf': 'C1',
            'column': '3',
            'row': 'Bottom',
            'status': 'available',
            'category': 'Poetry',
            'description': 'Dante\'s journey through Hell, Purgatory, and Paradise.'
        },
        {
            'title': 'Don Quixote',
            'author': 'Miguel de Cervantes',
            'isbn': '9780142437230',
            'publication_year': 1605,
            'publisher': 'Penguin Classics',
            'shelf': 'C2',
            'column': '1',
            'row': 'Top',
            'status': 'available',
            'category': 'Fiction',
            'description': 'The adventures of the man from La Mancha.'
        },
        {
            'title': 'Anna Karenina',
            'author': 'Leo Tolstoy',
            'isbn': '9780143035008',
            'publication_year': 1877,
            'publisher': 'Penguin Classics',
            'shelf': 'C2',
            'column': '2',
            'row': 'Middle',
            'status': 'available',
            'category': 'Fiction',
            'description': 'Acclaimed as the greatest novel ever written.'
        },
        {
            'title': 'Les Misérables',
            'author': 'Victor Hugo',
            'isbn': '9780451419439',
            'publication_year': 1862,
            'publisher': 'Signet Classics',
            'shelf': 'C2',
            'column': '3',
            'row': 'Bottom',
            'status': 'available',
            'category': 'Fiction',
            'description': 'The timeless story of Jean Valjean, Bishop Myriel, and Inspector Javert.'
        },
        {
            'title': 'War and Peace',
            'author': 'Leo Tolstoy',
            'isbn': '9781400079988',
            'publication_year': 1869,
            'publisher': 'Vintage',
            'shelf': 'D1',
            'column': '1',
            'row': 'Top',
            'status': 'available',
            'category': 'Fiction',
            'description': 'Epic story of Russian society during the Napoleonic era.'
        },
        {
            'title': 'Crime and Punishment',
            'author': 'Fyodor Dostoevsky',
            'isbn': '9780143058144',
            'publication_year': 1866,
            'publisher': 'Penguin Classics',
            'shelf': 'D1',
            'column': '2',
            'row': 'Middle',
            'status': 'issued',
            'category': 'Fiction',
            'description': 'The story of Raskolnikov, a poor student who murders a pawnbroker.'
        },
        {
            'title': 'The Brothers Karamazov',
            'author': 'Fyodor Dostoevsky',
            'isbn': '9780374528379',
            'publication_year': 1880,
            'publisher': 'Farrar, Straus and Giroux',
            'shelf': 'D1',
            'column': '3',
            'row': 'Bottom',
            'status': 'available',
            'category': 'Fiction',
            'description': 'A passionate philosophical novel that enters deeply into questions of God, free will, and morality.'
        },
        {
            'title': 'One Hundred Years of Solitude',
            'author': 'Gabriel García Márquez',
            'isbn': '9780060883287',
            'publication_year': 1967,
            'publisher': 'Harper Perennial',
            'shelf': 'D2',
            'column': '1',
            'row': 'Top',
            'status': 'available',
            'category': 'Fiction',
            'description': 'The multi-generational story of the Buendía family in the fictional town of Macondo.'
        },
        {
            'title': 'The Picture of Dorian Gray',
            'author': 'Oscar Wilde',
            'isbn': '9780141439570',
            'publication_year': 1890,
            'publisher': 'Penguin Classics',
            'shelf': 'D2',
            'column': '2',
            'row': 'Middle',
            'status': 'available',
            'category': 'Fiction',
            'description': 'The story of a young man who sells his soul for eternal youth and beauty.'
        },
        {
            'title': 'Wuthering Heights',
            'author': 'Emily Brontë',
            'isbn': '9780141439556',
            'publication_year': 1847,
            'publisher': 'Penguin Classics',
            'shelf': 'D2',
            'column': '3',
            'row': 'Bottom',
            'status': 'available',
            'category': 'Fiction',
            'description': 'The story of the doomed love between Catherine Earnshaw and Heathcliff.'
        },
        {
            'title': 'The Count of Monte Cristo',
            'author': 'Alexandre Dumas',
            'isbn': '9780140449266',
            'publication_year': 1844,
            'publisher': 'Penguin Classics',
            'shelf': 'E1',
            'column': '1',
            'row': 'Top',
            'status': 'available',
            'category': 'Fiction',
            'description': 'A tale of suffering, punishment, vengeance, and redemption.'
        },
        {
            'title': 'The Canterbury Tales',
            'author': 'Geoffrey Chaucer',
            'isbn': '9780140424386',
            'publication_year': 1400,
            'publisher': 'Penguin Classics',
            'shelf': 'E1',
            'column': '2',
            'row': 'Middle',
            'status': 'available',
            'category': 'Poetry',
            'description': 'A collection of 24 stories that are presented as part of a story-telling contest.'
        },
        {
            'title': 'Alice\'s Adventures in Wonderland',
            'author': 'Lewis Carroll',
            'isbn': '9780141439761',
            'publication_year': 1865,
            'publisher': 'Penguin Classics',
            'shelf': 'E1',
            'column': '3',
            'row': 'Bottom',
            'status': 'issued',
            'category': 'Fiction',
            'description': 'The story of a girl named Alice who falls down a rabbit hole into a fantasy world.'
        },
        {
            'title': 'The Art of War',
            'author': 'Sun Tzu',
            'isbn': '9780140439199',
            'publication_year': -500,
            'publisher': 'Penguin Classics',
            'shelf': 'E2',
            'column': '1',
            'row': 'Top',
            'status': 'available',
            'category': 'Philosophy',
            'description': 'An ancient Chinese military treatise dating from the 5th century BC.'
        },
        {
            'title': 'The Republic',
            'author': 'Plato',
            'isbn': '9780140455113',
            'publication_year': -380,
            'publisher': 'Penguin Classics',
            'shelf': 'E2',
            'column': '2',
            'row': 'Middle',
            'status': 'available',
            'category': 'Philosophy',
            'description': 'A Socratic dialogue, written by Plato around 380 BC, concerning justice.'
        }
    ]
    
    # Add books to the database
    for book_data in books:
        book = Book(**book_data)
        db.session.add(book)
    
    # Commit the changes
    db.session.commit()
