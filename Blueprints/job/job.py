from flask import Blueprint, jsonify, request

from .job_models import Job, JobSchema
from Blueprints.user.helper_functions import verify_jwt

job_bp = Blueprint('job', __name__)

@job_bp.route('/view_all', methods=['GET'])
def view_all():
    jobs = Job.query.all()
    jobSchema = JobSchema()
    jobs = jobSchema.dump(jobs, many=True)
    return jsonify(jobs)


@job_bp.route('/add', methods=['POST'])
def add():
    headers = request.headers
    bearer = headers.get('Authorization')
    if not bearer:
        return jsonify({
            'Error': 'No Authentication Token Found'
        }), 401
    

    token = bearer.split()[1]
    
    verification_payload = verify_jwt(token)
    return jsonify(verification_payload) 

    return jsonify({'Token': token})