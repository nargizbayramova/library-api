from datetime import date,timedelta
from repositories import loans as repo, books, members
from errors import error_response
from notifications import notify
from utils.validation import check
from utils.checks import money, loan_limit
from utils.fines import calculate_fine

def serialize(row, current=False):
    body={"id":row[0],"book_id":row[1],"member_id":row[2],"due_date":row[3],"returned":bool(row[4]),"fine":money(row[5]),"fine_paid":bool(row[6]),"renewals":row[7],"checked_out":row[8]}
    if current: body["current_fine"]=money(row[5] if row[4] else calculate_fine(row[3]))
    return body
def list_loans(overdue=False):
    result=[]
    for row in repo.list_loans():
        late=(date.today()-date.fromisoformat(row[3])).days
        if overdue and (row[4] or late<=0):continue
        result.append(serialize(row,True))
    return result
def get_loan(loan_id):
    row=repo.get_loan(loan_id); return (serialize(row,True),200) if row else error_response("loan not found",404)
def create_loan(data):
    if not data.get("book_id") or not data.get("member_id"):return error_response("book_id and member_id are required",400)
    if data.get("due_date") and not check(data["due_date"],"date"):return error_response("invalid due_date",400)
    book=books.get_book(data["book_id"])
    if book is None:return error_response("book not found",404)
    member=members.get_member(data["member_id"])
    if member is None:return error_response("member not found",404)
    if book[4]==0:return error_response("book is not available",409)
    rows=repo.member_loans(data["member_id"]); opened=sum(r[4]==0 for r in rows)
    owed=sum(calculate_fine(r[3]) for r in rows if r[4]==0)+sum(r[5] for r in rows if r[4] and not r[6])
    if owed>0:return error_response("member has unpaid fines",409)
    if opened>=loan_limit(member[3]):return error_response("loan limit reached",409)
    today=date.today(); due=data.get("due_date") or (today+timedelta(days=14)).isoformat()
    row=repo.create_loan(data["book_id"],data["member_id"],due,today.isoformat())
    notify(member[2],"checkout",book[1]); return serialize(row),201
def return_book(loan_id):
    row=repo.get_loan(loan_id)
    if row is None:return error_response("loan not found",404)
    if row[4]:return error_response("loan already returned",409)
    fine=calculate_fine(row[3]); updated=repo.return_loan(loan_id,row[1],fine)
    member=members.get_member(row[2]); book=books.get_book(row[1]); notify(member[2],"return",book[1],money(fine))
    return serialize(updated)
def renew_loan(loan_id):
    row=repo.get_loan(loan_id)
    if row is None:return error_response("loan not found",404)
    if row[4]:return error_response("loan already returned",409)
    if date.fromisoformat(row[3])<date.today():return error_response("overdue loans cannot be renewed",409)
    if row[7]>=1:return error_response("loan was already renewed",409)
    updated=repo.renew_loan(loan_id,(date.fromisoformat(row[3])+timedelta(days=14)).isoformat())
    member=members.get_member(row[2]); book=books.get_book(row[1]); notify(member[2],"renew",book[1]); return serialize(updated)
def pay_fine(loan_id):
    row=repo.get_loan(loan_id)
    if row is None:return error_response("loan not found",404)
    if not row[4]:return error_response("return the book before paying",409)
    if row[5]<=0 or row[6]:return error_response("no fine to pay",409)
    updated=repo.pay_fine(loan_id); member=members.get_member(row[2]); notify(member[2],"fine_paid",fine=money(row[5])); return serialize(updated)
def overdue_report():
    items=[]; total=0
    for row in repo.overdue_report_rows():
        days=(date.today()-date.fromisoformat(row[3])).days
        if days>0:
            fine=calculate_fine(row[3]);total+=fine;items.append({"loan_id":row[0],"title":row[1],"member":row[2],"days_late":days,"fine":money(fine)})
    return {"items":items,"total_fines":money(total)}
def summary():
    rows=repo.list_loans(); opened=sum(r[4]==0 for r in rows)
    outstanding=sum(calculate_fine(r[3]) for r in rows if r[4]==0)+sum(r[5] for r in rows if r[4] and not r[6])
    return {"total_books":books.book_count(),"on_loan":opened,"fines_outstanding":money(outstanding)}
