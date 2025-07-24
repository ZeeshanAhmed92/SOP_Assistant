from datetime import datetime, time
from employees.models.employees import Schedule
from configs.db import db

def is_on_shift(employee_id):
    now = datetime.now()
    today = now.date()
    current_time = now.time()

    shift = Schedule.query.filter_by(
        employee_id=employee_id,
        shift_date=today
    ).filter(
        Schedule.start_time <= current_time,
        Schedule.end_time >= current_time
    ).first()

    return shift is not None
