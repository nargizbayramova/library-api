from repositories.db import connect

def list_books(available_only=False):
    with connect() as conn:
        query = "SELECT * FROM books WHERE available = 1" if available_only else "SELECT * FROM books"
        return conn.execute(query).fetchall()

def get_book(book_id):
    with connect() as conn: return conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()

def create_book(title, author, isbn):
    with connect() as conn:
        cur = conn.execute("INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)", (title, author, isbn))
        return conn.execute("SELECT * FROM books WHERE id = ?", (cur.lastrowid,)).fetchone()

def delete_book(book_id):
    with connect() as conn: conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
