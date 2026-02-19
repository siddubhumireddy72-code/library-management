"""
Database Models for Library Management System
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Book(db.Model):
    """Book model"""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    borrowings = db.relationship('Borrowing', backref='book', lazy=True)
    
    def __repr__(self):
        return f'<Book {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'category': self.category,
            'quantity': self.quantity,
            'available_copies': self.available_copies,
            'description': self.description
        }


class Member(db.Model):
    """Member model"""
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    borrowings = db.relationship('Borrowing', backref='member', lazy=True)
    
    def __repr__(self):
        return f'<Member {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address
        }


class Borrowing(db.Model):
    """Borrowing/Loan model"""
    __tablename__ = 'borrowings'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='borrowed')  # borrowed, returned
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Borrowing Book:{self.book_id} Member:{self.member_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'borrow_date': self.borrow_date.strftime('%Y-%m-%d'),
            'due_date': self.due_date.strftime('%Y-%m-%d'),
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else None,
            'status': self.status
        }
    
    @property
    def is_overdue(self):
        """Check if the borrowing is overdue"""
        if self.status == 'borrowed':
            return datetime.now() > self.due_date
        return False
    
    @property
    def days_overdue(self):
        """Get number of days overdue"""
        if self.is_overdue:
            return (datetime.now() - self.due_date).days
        return 0
