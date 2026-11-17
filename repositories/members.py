from repositories.db import connect

def list_members():
    with connect() as conn: return conn.execute("SELECT * FROM members").fetchall()

def get_member(member_id):
    with connect() as conn: return conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()

def member_by_email(email):
    with connect() as conn: return conn.execute("SELECT * FROM members WHERE email = ?", (email,)).fetchone()

def create_member(name, email, member_type):
    with connect() as conn:
        cur = conn.execute("INSERT INTO members (name, email, type) VALUES (?, ?, ?)", (name, email, member_type))
        return conn.execute("SELECT * FROM members WHERE id = ?", (cur.lastrowid,)).fetchone()
