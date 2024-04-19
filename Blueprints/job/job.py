from flask import Blueprint, jsonify, request

from .job_models import Job, JobSchema
from Blueprints.user.helper_functions import require_auth
from Blueprints.user.user_models import User
from .helper_functions import str_to_list

from database import db

job_bp = Blueprint('job', __name__)

@job_bp.route('/view_all/<start>', methods=['GET'])
def view_all(start):
    jobs = Job.query.offset(start).limit(2)
    jobSchema = JobSchema()
    jobs = jobSchema.dump(jobs, many=True)
    for job in jobs:
        job['appliers'] = str_to_list(job['appliers'])
    return jsonify(jobs)

@job_bp.route('/all_user_jobs')
def all_user_jobs():
    verification_payload = require_auth(request)
    if "error" in verification_payload:
        return jsonify({'error': verification_payload['error']})
    
    user_id = verification_payload['user_id']
    user = User.query.get(user_id)
    jobs = Job.query.filter_by(posted_by=user.username)
    jobSchema = JobSchema()
    jobs = jobSchema.dump(jobs, many=True)
    for job in jobs:
        job['appliers'] = str_to_list(job['appliers'])
    return jsonify(jobs)

@job_bp.route('all_job_appliers/<job_id>')
def all_job_appliers(job_id):
    verification_payload = require_auth(request)
    if "error" in verification_payload:
        return jsonify({'error': verification_payload['error']})
    
    user_id = verification_payload['user_id']
    user = User.query.get(user_id)

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job With Id ' + job_id + ' does not exist'})
    if job.posted_by != user.username:
        return jsonify({'error': 'Not Authorized'})
    

    appliers_ids = str_to_list(job.appliers)
    appliers = []
    for i in range(len(appliers_ids)):
        user = User.query.get(appliers_ids[i])
        appliers.append({
            "id": appliers_ids[i],
            "username": user.username,
            "fullname": user.full_name,
            "email": user.email
        })


    return jsonify(appliers)

@job_bp.route('/add', methods=['POST'])
def add():
    verification_payload = require_auth(request)
    if "error" in verification_payload:
        return jsonify({'error': verification_payload['error']})
    
    user_id = verification_payload['user_id']
    user = User.query.get(user_id)
    
    data = request.json
    
    title = data.get('title')
    body = data.get('body')

    if not title or len(title)==0:
        return jsonify({
            'error': 'A title is required'
        })
    if not body or len(body)==0:
        return jsonify({
            'error': 'A description is required'
        })
    posted_by = user.username

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