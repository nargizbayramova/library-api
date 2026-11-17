def money(value):
    return round(float(value), 2)

def loan_limit(member_type):
    return 5 if member_type == "staff" else 3
