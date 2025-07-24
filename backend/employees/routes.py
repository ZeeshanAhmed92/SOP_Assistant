from flask import Blueprint, request, jsonify
from employees.models.employees import Employee
from employees.models.employees import Schedule
from configs.db import db
from datetime import datetime

emp_bp = Blueprint('employee', __name__)

@emp_bp.route('/add', methods=['POST'])
def add_employee():
    data = request.json
    emp = Employee(
        business_id=data['business_id'],
        location_id=data['location_id'],
        name=data['name'],
        role=data['role'],
        email=data['email'],
        phone=data.get('phone'),
        dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d')
    )
    db.session.add(emp)
    db.session.commit()
    return jsonify({'message': 'Employee added successfully'})

@emp_bp.route('/schedule', methods=['POST'])
def add_schedule():
    data = request.json
    sched = Schedule(
        employee_id=data['employee_id'],
        location_id=data['location_id'],
        shift_date=datetime.strptime(data['shift_date'], '%Y-%m-%d').date(),
        start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
        end_time=datetime.strptime(data['end_time'], '%H:%M').time()
    )
    db.session.add(sched)
    db.session.commit()
    return jsonify({'message': 'Schedule added successfully'})