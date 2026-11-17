from flask import Blueprint,request,jsonify
from services import loans
bp=Blueprint('loans',__name__)
@bp.get('/loans')
def list_loans(): return jsonify(loans.list_loans(request.args.get('overdue')=='true'))
@bp.get('/loans/<int:loan_id>')
def get_loan(loan_id):
    result=loans.get_loan(loan_id)
    return (jsonify(result[0]),result[1]) if isinstance(result,tuple) and len(result)==2 and isinstance(result[0],dict) else result
@bp.post('/loans')
def create_loan():
    result=loans.create_loan(request.get_json(silent=True) or {})
    return (jsonify(result[0]),result[1]) if isinstance(result,tuple) and len(result)==2 and isinstance(result[0],dict) else result
@bp.post('/loans/<int:loan_id>/return')
def return_book(loan_id):
    result=loans.return_book(loan_id)
    return jsonify(result) if isinstance(result,dict) else result
@bp.post('/loans/<int:loan_id>/renew')
def renew_loan(loan_id):
    result=loans.renew_loan(loan_id)
    return jsonify(result) if isinstance(result,dict) else result
@bp.post('/loans/<int:loan_id>/pay-fine')
def pay_fine(loan_id):
    result=loans.pay_fine(loan_id)
    return jsonify(result) if isinstance(result,dict) else result
