from repositories import books as repo
from errors import error_response
from utils.validation import check

def serialize(row):
    return {"id": row[0], "title": row[1], "author": row[2], "isbn": row[3], "available": bool(row[4])}
def list_books(available): return [serialize(r) for r in repo.list_books(available)]
def get_book(book_id):
    row=repo.get_book(book_id)
    return (serialize(row), 200) if row else error_response("book not found",404)
def create_book(data):
    if not data.get("title") or not data.get("author"): return error_response("title and author are required",400)
    if not check(data.get("isbn"),"isbn"): return error_response("invalid isbn",400)
    return serialize(repo.create_book(data["title"],data["author"],data["isbn"])),201
def delete_book(book_id):
    row=repo.get_book(book_id)
    if row is None:return error_response("book not found",404)
    if row[4]==0:return error_response("book is on loan",409)
    repo.delete_book(book_id); return "",204
