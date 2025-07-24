from flask import Blueprint, request, jsonify
from auth.utils import generate_token, verify_user
from employees.models.employees import Employee

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    pin = data.get('pin')  # assuming PIN-based login

    user = verify_user(email, pin)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    token = generate_token(user)
    return jsonify({'token': token, 'role': user.role})
