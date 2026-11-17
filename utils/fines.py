from datetime import date

FINE_PER_DAY = 0.50

def calculate_fine(due_date, on_date=None):
    today = on_date or date.today()
    days_late = (today - date.fromisoformat(due_date)).days
    return max(0, days_late) * FINE_PER_DAY
