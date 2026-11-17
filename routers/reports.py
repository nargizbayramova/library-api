from flask import Blueprint,jsonify
from services.loans import overdue_report,summary
bp=Blueprint('reports',__name__)
@bp.get('/reports/overdue')
def report_overdue(): return jsonify(overdue_report())
@bp.get('/reports/summary')
def report_summary(): return jsonify(summary())
