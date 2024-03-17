#!/usr/bin/python3
"""API handler for teachers"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.teacher import Teacher
from api.v1.views import limiter


session = storage.get_session()
@app_views.route("/teachers", methods=['GET', 'POST'], strict_slashes=False)
@limiter.limit("1 per minute")
def teachers():
    """
    method to manage teachers
		GET: returns all teachers
		POST: creates a new teacher
    """
    if request.method == "GET":
        teachers = [teacher.to_dict() for teacher in storage.all(Teacher).values()]
        return jsonify(teachers)
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if data:
            new_teacher = {}
            if "first_name" not in data:
                abort(400, "first_name missing")
            new_teacher["first_name"] = data["first_name"]
            if "last_name" not in data:
                abort(400, "last_name missing")
            new_teacher["last_name"] = data["last_name"]
            if "email" not in data:
                abort(400, "email missing")
            new_teacher["email"] = data["email"]
            if "password" not in data:
                abort(400, "password missing")
            new_teacher["password"] = data["password"]
            if "matricule" not in data:
                abort(400, "matricule missing")
            session = storage.get_session()
            matricules = session.query(Teacher.matricule).all()
            # Extract matricules from the result
            matricule_list = [matricule[0] for matricule in matricules]
            
            if data["matricule"] in matricule_list:
                abort(400, "Teacher with matricule {} already exist".format(data["matricule"]))
            new_teacher["matricule"] = data["matricule"]
            if "grade" not in data:
                abort(400, "grade missing")
            new_teacher["grade"] = data["grade"]
            if "position" not in data:
                abort(400, "position missing")
            new_teacher["position"] = data["position"]

            teacher = Teacher(**new_teacher)
            teacher.save()
            return jsonify(teacher.to_dict()), 201
    

        
            
@app_views.route("/teacher/<teacher_id>",  methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_teacher(teacher_id):
    """
    method to manage teacher by  ID
		GET: get a teacher by their ID
		DELETE: delete a teacher by their ID
  		UPDATE: updates an existing teacher with ID
    """
    teacher = storage.get(Teacher, teacher_id)
    if teacher is None:
        abort(404)
    if request.method == "GET":
        return jsonify(teacher.to_dict())
    
    elif request.method == "DELETE":
        storage.delete(teacher)
        storage.save()
        return {}, 200

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(404, "Not a JSON")
        for attribute, value in data.items():
            if attribute not in ['id', 'created_at', 'updated_at']:
                setattr(teacher, attribute, value)
        teacher.save()
        return jsonify(teacher.to_dict()), 201

@app_views.route("/teacher/info/<teacher_id>",  methods=['GET'], strict_slashes=False)
def get_teacher_info(teacher_id):
    """
    method to retrieve all information about a teacher
		GET: gets all information related to a teacher
    """
    import requests
    teacher_details = {}
    
    # section to manage personal information

    teacher = storage.get(Teacher, teacher_id)
    if teacher is None:
            teacher = session.query(Teacher).filter_by(matricule=teacher_id).first()
            if teacher is None:
                abort(404)
    teacher_info = {}
    teacher_info["matricule"] = teacher.matricule
    teacher_info["grade"] = teacher.grade
    teacher_info["position"] = teacher.position
    teacher_info["created_at"] = teacher.created_at
    teacher_info["updated_at"] = teacher.updated_at
    teacher_details["teacher_info"] = teacher_info
  
    #from models.personnel import Personnel
    # personnel = session.query(Personnel).filter_by(id=teacher["id"]).first()
    personnel = teacher.personnel

    personal_info = {}
    personal_info["First_Name"] = personnel.first_name
    personal_info["Last_Name"] = personnel.last_name
    personal_info["Email"] = personnel.email
    personal_info["id"] = personnel.id
    personal_info["user_type"] = teacher.__class__.__name__
    
    teacher_details["personal_info"] = personal_info

    course_info = []
    record = {}
    for course in teacher.courses:
        record["code"] = course.code
        record["title"] = course.title
        record["coeff"] = course.coeff
        record["class_id"] = course.class_id
        course_info.append(record.copy())
    teacher_details["courses"] = course_info

    
    return jsonify(teacher_details), 200