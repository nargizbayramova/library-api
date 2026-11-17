from flask import Blueprint,request,jsonify
from services import books
bp=Blueprint('books',__name__)
@bp.get('/books')
def list_books(): return jsonify(books.list_books(request.args.get('available')=='true'))
@bp.get('/books/<int:book_id>')
def get_book(book_id):
    result=books.get_book(book_id)
    return (jsonify(result[0]),result[1]) if isinstance(result,tuple) and len(result)==2 and isinstance(result[0],dict) else result
@bp.post('/books')
def create_book():
    result=books.create_book(request.get_json(silent=True) or {})
    return (jsonify(result[0]),result[1]) if isinstance(result,tuple) and len(result)==2 and isinstance(result[0],dict) else result
@bp.delete('/books/<int:book_id>')
def delete_book(book_id): return books.delete_book(book_id)
