from repositories import members as repo, loans
from errors import error_response
from utils.validation import check
from utils.checks import money
from utils.fines import calculate_fine
from datetime import date

def serialize(row): return {"id":row[0],"name":row[1],"email":row[2],"type":row[3]}
def list_members(): return [serialize(r) for r in repo.list_members()]
def get_member(member_id):
    row=repo.get_member(member_id); return (serialize(row),200) if row else error_response("member not found",404)
def create_member(data):
    if not data.get("name"): return error_response("name is required",400)
    if not check(data.get("email"),"email"): return error_response("invalid email",400)
    kind=data.get("type","student")
    if not check(kind,"member_type"): return error_response("type must be student or staff",400)
    if repo.member_by_email(data["email"]): return error_response("email already registered",409)
    return serialize(repo.create_member(data["name"],data["email"],kind)),201
def member_loans(member_id):
    member=repo.get_member(member_id)
    if not member:return error_response("member not found",404)
    rows=loans.member_loans(member_id); owed=0; opened=0; result=[]
    for loan in rows:
        if loan[4]==0:
            opened+=1; owed+=calculate_fine(loan[3])
        elif loan[6]==0: owed+=loan[5]
        result.append({"id":loan[0],"book_id":loan[1],"due_date":loan[3],"returned":bool(loan[4]),"fine":money(loan[5]),"fine_paid":bool(loan[6])})
    return {"loans":result,"total_owed":money(owed),"loans_remaining":(5 if member[3]=="staff" else 3)-opened}
