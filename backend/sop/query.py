from flask import Blueprint, request, jsonify
from .processor import query_index
from employees.scheduler import is_on_shift
import traceback

sop_query_bp = Blueprint('sop_query', __name__)

@sop_query_bp.route('/query', methods=['POST'])
def query_sop():
    data = request.json
    question = data.get('question')
    employee_id = data.get('employee_id')

    if not question or not employee_id:
        return jsonify({'error': 'Both employee_id and question are required'}), 400

    try:
        print(f"[DEBUG] Received question: {question} from employee {employee_id}")

        # ✅ Check if employee is on shift
        if not is_on_shift(employee_id):
            return jsonify({'error': 'Employee is not currently on shift'}), 403

        answer = query_index(question)
        print(f"[DEBUG] Answer: {answer}")
        return jsonify({'response': answer})

    except Exception as e:
        print("[ERROR] Exception in /query route")
        traceback.print_exc()
        return jsonify({'error': str(e) or "Unknown error occurred"}), 500