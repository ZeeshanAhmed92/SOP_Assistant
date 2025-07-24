import jwt
from datetime import datetime, timedelta
from employees.models.employees import Employee
from configs.configurations import SECRET_KEY

def generate_token(user):
    payload = {
        'sub': user.employee_id,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_user(email, pin):
    # This would check against a real PIN or password in production
    user = Employee.query.filter_by(email=email).first()
    if user and pin == '1234':  # Example PIN check
        return user
    return None

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
