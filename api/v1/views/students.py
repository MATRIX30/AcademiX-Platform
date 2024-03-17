#!/usr/bin/python3
"""API handler for students"""
from api.v1.views import app_views, make_remark
from models import storage
from flask import jsonify, abort, request
from models.student import Student
from api.v1.views import limiter

session = storage.get_session()

@app_views.route("/students", methods=['GET', 'POST'], strict_slashes=False)
@limiter.limit("1 per minute")
def students():
    """
    method to manage students
		GET: returns all students
		POST: creates a new student
    """
    if request.method == "GET":
        students = [student.to_dict() for student in storage.all(Student).values()]
        return jsonify(students)
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if data:
            new_student = {}
            if "first_name" not in data:
                abort(400, "first_name missing")
            new_student["first_name"] = data["first_name"]
            if "last_name" not in data:
                abort(400, "last_name missing")
            new_student["last_name"] = data["last_name"]
            if "registration_number" not in data:
                abort(400, "registration_number missing")
            new_student["registration_number"] = data["registration_number"]
            if "class_id" not in data:
                abort(400, "class_id missing")
                
            # check if its a valid class_id
            valid_class_keys = storage.all("Class").values()
            valid_class_ids = [item.code for item in valid_class_keys]
            if data["class_id"] not in valid_class_ids:
                abort(400, "class_id doesn't reference a valid class")
            new_student["class_id"] = data["class_id"]
            if "email" not in data:
                abort(400, "email missing")
            new_student["email"] = data["email"]
            if "password" not in data:
                abort(400, "password missing")
            new_student["password"] = data["password"]
            
            student = Student(**new_student)
            student.save()
            return jsonify(student.to_dict()), 201
    
            
@app_views.route("/student/<student_id>",  methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_student(student_id):
    """
    method to manage student by  ID
		GET: get a student by their ID
		DELETE: delete a student by their ID
  		UPDATE: updates an existing student with ID
    """
    student = storage.get(Student, student_id)
    if student is None:
        student = session.query(Student).filter_by(registration_number=student_id).first()
        if student is None:
            abort(404)
    if student is None:
        abort(404)
    if request.method == "GET":
        return jsonify(student.to_dict())
    
    elif request.method == "DELETE":
        storage.delete(student)
        storage.save()
        return {}, 200

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(404, "Not a JSON")
        for attribute, value in data.items():
            if attribute not in ['id', 'created_at', 'updated_at']:
                setattr(student, attribute, value)
        student.save()
        return jsonify(student.to_dict()), 201

@app_views.route("/student/<student_id>/courses",  methods=['GET'], strict_slashes=False)
def get_student_courses(student_id):
    """
    method to manage student by  ID
		GET: get the courses associate to a student with student_id
    """
    session = storage.get_session()
    student = storage.get(Student, student_id)
    if student is None:
            student = session.query(Student).filter_by(registration_number=student_id).first()
            if student is None:
                abort(404)
    course_list = [course.to_dict() for course in  student.courses]
    return course_list

@app_views.route("/student/info/<student_id>",  methods=['GET'], strict_slashes=False)
def get_student_info(student_id):
    """
    method to retrieve all information about a student
		GET: gets all information related to a student
    """
    import requests
    student_info = {}
    
    # section to manage personal information
    session = storage.get_session()
    student = storage.get(Student, student_id)
    if student is None:
            student = session.query(Student).filter_by(registration_number=student_id).first()
            if student is None:
                abort(404)
    personal_info = {}

    personal_info["First_Name"] = student.first_name
    personal_info["Last_Name"] = student.last_name
    personal_info["Student ID"] = student.registration_number
    personal_info["Class"] = student.class_id
    personal_info["Email"] = student.email
    personal_info["user_type"] = student.__class__.__name__
    
    academic_info = {}
    academic_info["courses"] = get_student_courses(student.registration_number)
    student_info["personal_info"] = personal_info
    student_info["academic_info"] = academic_info
    
    return jsonify(student_info), 200
    #return jsonify(personal_info), 200


@app_views.route("/student/results/<student_id>", methods=['GET'], strict_slashes=False)
def get_student_evaluation(student_id):
    """
    Method to get the evaluation results for all students in the course with course_id
    """
    from models.student import student_course
    # define a list to hold all the results
    student_result = []
    # the dictionary will contain dictionary of results for each student

    # get the list of courses for a student
    course_list = get_student_courses(student_id)
    course_ids  = [course["code"] for course in course_list]
    
    course_result = {}
    for course in course_list:
        course_result["code"] = course["code"]
        course_result["title"] = course["title"]
        course_result["coeff"] = course["coeff"]
        course_result["teacher_id"] = course["teacher_id"]
        course_result["class_id"] = course["class_id"]
        
        record = session.query(student_course).filter((student_course.c.student_id == student_id) & (student_course.c.course_id == course["code"])).first()
        course_result["first_term"] = [record[2], record[3], (record[2] + record[3])/2, make_remark((record[2] + record[3])/2)]
        course_result["second_term"] = [record[4], record[5], (record[4] + record[5])/2, make_remark((record[4] + record[5])/2)]
        course_result["third_term"] = [record[4], record[7], (record[6] + record[7])/2, make_remark((record[6] + record[7])/2)]
        student_result.append(course_result.copy())
    return student_result