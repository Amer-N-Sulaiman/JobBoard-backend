from flask import Blueprint, jsonify, request

from .job_models import Job, JobSchema
from Blueprints.user.helper_functions import require_auth

from database import db

job_bp = Blueprint('job', __name__)

@job_bp.route('/view_all', methods=['GET'])
def view_all():
    jobs = Job.query.all()
    jobSchema = JobSchema()
    jobs = jobSchema.dump(jobs, many=True)
    return jsonify(jobs)


@job_bp.route('/add', methods=['POST'])
def add():
    verification_payload = require_auth(request)
    if "error" in verification_payload:
        return jsonify({'error': verification_payload['error']})
    
    user_id = verification_payload['user_id']

    data = request.json

    title = data.get('title')
    body = data.get('body')
    posted_by = str(user_id)

    new_job = Job(title=title, body=body, posted_by=posted_by)

    db.session.add(new_job)
    db.session.commit()

    jobSchema = JobSchema()
    new_job = jobSchema.dump(new_job)

    return jsonify(new_job)

@job_bp.route('/apply/<job_id>')
def apply(job_id):
    verification_payload = require_auth(request)
    if "error" in verification_payload:
        return jsonify({'error': verification_payload['error']})
    
    user_id = verification_payload['user_id']

    job = Job.query.get(job_id)

    if job:

        appliers = job.appliers[1:-1]

        appliers_list = appliers.split(', ')

        if appliers_list[0]=='':
            appliers_list = appliers_list[1:]

        appliers_list = [int(x) for x in appliers_list]
        
        if user_id not in appliers_list:
            appliers_list.append(user_id)
            
        else:
            appliers_list.remove(user_id)
        
        appliers = str(appliers_list)
        job.appliers = appliers
        db.session.add(job)
        db.session.commit()
        jobSchema = JobSchema()
        job = jobSchema.dump(job)
        return jsonify(job)
    else:
        return jsonify({'error': 'job not found'})