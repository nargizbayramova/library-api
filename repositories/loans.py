from repositories.db import connect

def list_loans():
    with connect() as conn: return conn.execute("SELECT * FROM loans").fetchall()

def get_loan(loan_id):
    with connect() as conn: return conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()

def member_loans(member_id):
    with connect() as conn: return conn.execute("SELECT * FROM loans WHERE member_id = ?", (member_id,)).fetchall()

def create_loan(book_id, member_id, due_date, checked_out):
    with connect() as conn:
        cur = conn.execute("INSERT INTO loans (book_id, member_id, due_date, checked_out) VALUES (?, ?, ?, ?)", (book_id, member_id, due_date, checked_out))
        conn.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
        return conn.execute("SELECT * FROM loans WHERE id = ?", (cur.lastrowid,)).fetchone()

def return_loan(loan_id, book_id, fine):
    with connect() as conn:
        conn.execute("UPDATE loans SET returned = 1, fine = ? WHERE id = ?", (fine, loan_id))
        conn.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
        return conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()

def renew_loan(loan_id, due_date):
    with connect() as conn:
        conn.execute("UPDATE loans SET due_date = ?, renewals = renewals + 1 WHERE id = ?", (due_date, loan_id))
        return conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()

def pay_fine(loan_id):
    with connect() as conn:
        conn.execute("UPDATE loans SET fine_paid = 1 WHERE id = ?", (loan_id,))
        return conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()

def overdue_report_rows():
    with connect() as conn:
        return conn.execute("SELECT loans.id, books.title, members.name, loans.due_date FROM loans JOIN books ON books.id = loans.book_id JOIN members ON members.id = loans.member_id WHERE loans.returned = 0").fetchall()

def book_count():
    with connect() as conn: return conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
