from flask import Blueprint,request,jsonify
from services import members
bp=Blueprint('members',__name__)
@bp.get('/members')
def list_members(): return jsonify(members.list_members())
@bp.get('/members/<int:member_id>')
def get_member(member_id):
    result=members.get_member(member_id)
    return (jsonify(result[0]),result[1]) if isinstance(result,tuple) and len(result)==2 and isinstance(result[0],dict) else result
@bp.post('/members')
def create_member():
    result=members.create_member(request.get_json(silent=True) or {})
    return (jsonify(result[0]),result[1]) if isinstance(result,tuple) and len(result)==2 and isinstance(result[0],dict) else result
@bp.get('/members/<int:member_id>/loans')
def member_loans(member_id):
    result=members.member_loans(member_id)
    return jsonify(result) if isinstance(result,dict) else result
