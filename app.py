import os
import sqlite3
from datetime import date,timedelta
from flask import Flask
from routers.books import bp as books_bp
from routers.members import bp as members_bp
from routers.loans import bp as loans_bp
from routers.reports import bp as reports_bp

def init_db():
    conn=sqlite3.connect('library.db')
    conn.executescript('''
    DROP TABLE IF EXISTS books; DROP TABLE IF EXISTS members; DROP TABLE IF EXISTS loans;
    CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,author TEXT,isbn TEXT,available INTEGER DEFAULT 1);
    CREATE TABLE members (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT UNIQUE,type TEXT);
    CREATE TABLE loans (id INTEGER PRIMARY KEY AUTOINCREMENT,book_id INTEGER,member_id INTEGER,due_date TEXT,returned INTEGER DEFAULT 0,fine REAL DEFAULT 0,fine_paid INTEGER DEFAULT 0,renewals INTEGER DEFAULT 0,checked_out TEXT);
    ''')
    conn.executemany('INSERT INTO books (title,author,isbn,available) VALUES (?,?,?,?)',[
    ('Clean Code','Robert C. Martin','9780132350884',1),('The Pragmatic Programmer','Andrew Hunt','9780135957059',1),('Design Patterns','Erich Gamma','9780201633610',1),('Refactoring','Martin Fowler','9780134757599',1),('Code Complete','Steve McConnell','9780735619678',0)])
    conn.executemany('INSERT INTO members (name,email,type) VALUES (?,?,?)',[('Sam Rivera','sam@campus.edu','student'),('Dr. Noor Aziz','noor@campus.edu','staff'),('Alex Chen','alex@campus.edu','student')])
    today=date.today()
    conn.execute('INSERT INTO loans (book_id,member_id,due_date,checked_out) VALUES (5,3,?,?)',((today-timedelta(days=5)).isoformat(),(today-timedelta(days=19)).isoformat()))
    conn.commit();conn.close()

app=Flask(__name__)
app.register_blueprint(books_bp);app.register_blueprint(members_bp);app.register_blueprint(loans_bp);app.register_blueprint(reports_bp)
if not os.path.exists('library.db'): init_db()
