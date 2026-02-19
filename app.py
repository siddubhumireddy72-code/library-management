"""
Library Management System - Main Flask Application
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'library-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db and models from models
from models import db, Book, Member, Borrowing

# Initialize db with app
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Dashboard - Show statistics"""
    total_books = Book.query.count()
    total_members = Member.query.count()
    borrowed_books = Borrowing.query.filter_by(status='borrowed').count()
    overdue_books = Borrowing.query.filter(
        Borrowing.status == 'borrowed',
        Borrowing.due_date < datetime.now()
    ).count()
    
    recent_borrowings = Borrowing.query.order_by(Borrowing.borrow_date.desc()).limit(5).all()
    
    return render_template('index.html',
                         total_books=total_books,
                         total_members=total_members,
                         borrowed_books=borrowed_books,
                         overdue_books=overdue_books,
                         recent_borrowings=recent_borrowings)


# Book Routes
@app.route('/books')
def books():
    """List all books"""
    search_query = request.args.get('search', '')
    if search_query:
        books = Book.query.filter(
            (Book.title.contains(search_query)) |
            (Book.author.contains(search_query)) |
            (Book.isbn.contains(search_query))
        ).all()
    else:
        books = Book.query.all()
    return render_template('books.html', books=books, search_query=search_query)


@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    """Add a new book"""
    if request.method == 'POST':
        book = Book(
            title=request.form['title'],
            author=request.form['author'],
            isbn=request.form['isbn'],
            category=request.form['category'],
            quantity=int(request.form['quantity']),
            description=request.form.get('description', '')
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books'))
    return render_template('add_book.html')


@app.route('/books/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    """Edit a book"""
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.category = request.form['category']
        book.quantity = int(request.form['quantity'])
        book.description = request.form.get('description', '')
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books'))
    return render_template('edit_book.html', book=book)


@app.route('/books/delete/<int:id>')
def delete_book(id):
    """Delete a book"""
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('books'))


# Member Routes
@app.route('/members')
def members():
    """List all members"""
    search_query = request.args.get('search', '')
    if search_query:
        members = Member.query.filter(
            (Member.name.contains(search_query)) |
            (Member.email.contains(search_query)) |
            (Member.phone.contains(search_query))
        ).all()
    else:
        members = Member.query.all()
    return render_template('members.html', members=members, search_query=search_query)


@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    """Add a new member"""
    if request.method == 'POST':
        member = Member(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            address=request.form.get('address', '')
        )
        db.session.add(member)
        db.session.commit()
        flash('Member added successfully!', 'success')
        return redirect(url_for('members'))
    return render_template('add_member.html')


@app.route('/members/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    """Edit a member"""
    member = Member.query.get_or_404(id)
    if request.method == 'POST':
        member.name = request.form['name']
        member.email = request.form['email']
        member.phone = request.form['phone']
        member.address = request.form.get('address', '')
        db.session.commit()
        flash('Member updated successfully!', 'success')
        return redirect(url_for('members'))
    return render_template('edit_member.html', member=member)


@app.route('/members/delete/<int:id>')
def delete_member(id):
    """Delete a member"""
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted successfully!', 'success')
    return redirect(url_for('members'))


# Borrowing Routes
@app.route('/borrow')
def borrow_books():
    """List all borrowings"""
    filter_status = request.args.get('status', 'all')
    if filter_status == 'borrowed':
        borrowings = Borrowing.query.filter_by(status='borrowed').all()
    elif filter_status == 'returned':
        borrowings = Borrowing.query.filter_by(status='returned').all()
    elif filter_status == 'overdue':
        borrowings = Borrowing.query.filter(
            Borrowing.status == 'borrowed',
            Borrowing.due_date < datetime.now()
        ).all()
    else:
        borrowings = Borrowing.query.all()
    return render_template('borrow.html', borrowings=borrowings, filter_status=filter_status)


@app.route('/borrow/issue', methods=['GET', 'POST'])
def issue_book():
    """Issue a book to a member"""
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        member_id = int(request.form['member_id'])
        days = int(request.form.get('days', 14))
        
        book = Book.query.get(book_id)
        member = Member.query.get(member_id)
        
        if book and book.available_copies > 0:
            borrowing = Borrowing(
                book_id=book_id,
                member_id=member_id,
                borrow_date=datetime.now(),
                due_date=datetime.now() + timedelta(days=days),
                status='borrowed'
            )
            book.available_copies -= 1
            db.session.add(borrowing)
            db.session.commit()
            flash(f'Book "{book.title}" issued to {member.name}!', 'success')
        else:
            flash('Book not available or invalid!', 'error')
        return redirect(url_for('borrow_books'))
    
    books = Book.query.filter(Book.available_copies > 0).all()
    members = Member.query.all()
    return render_template('issue_book.html', books=books, members=members)


@app.route('/borrow/return/<int:id>')
def return_book(id):
    """Return a borrowed book"""
    borrowing = Borrowing.query.get_or_404(id)
    if borrowing.status == 'borrowed':
        book = Book.query.get(borrowing.book_id)
        book.available_copies += 1
        borrowing.return_date = datetime.now()
        borrowing.status = 'returned'
        db.session.commit()
        flash('Book returned successfully!', 'success')
    return redirect(url_for('borrow_books'))


# API Routes for dynamic content
@app.route('/api/book/<int:id>')
def get_book(id):
    """Get book details as JSON"""
    book = Book.query.get(id)
    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'category': book.category,
            'available': book.available_copies,
            'total': book.quantity
        })
    return jsonify({'error': 'Book not found'}), 404


@app.route('/api/member/<int:id>')
def get_member(id):
    """Get member details as JSON"""
    member = Member.query.get(id)
    if member:
        return jsonify({
            'id': member.id,
            'name': member.name,
            'email': member.email,
            'phone': member.phone
        })
    return jsonify({'error': 'Member not found'}), 404


# Search Route
@app.route('/search')
def search():
    """Search books and members"""
    query = request.args.get('q', '')
    if query:
        books = Book.query.filter(
            (Book.title.contains(query)) |
            (Book.author.contains(query)) |
            (Book.isbn.contains(query))
        ).all()
        members = Member.query.filter(
            (Member.name.contains(query)) |
            (Member.email.contains(query)) |
            (Member.phone.contains(query))
        ).all()
    else:
        books = []
        members = []
    return render_template('search.html', books=books, members=members, query=query)


if __name__ == '__main__':
    app.run(debug=True)
