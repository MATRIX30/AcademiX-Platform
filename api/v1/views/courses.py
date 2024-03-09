#!/usr/bin/python3
"""API handler for Courses"""
from api.v1.views import app_views, make_remark
from models import storage
from flask import jsonify, abort, request
from models.course import Course
from api.v1.views import limiter


session = storage.get_session()
@app_views.route("/courses", methods=['GET', 'POST'], strict_slashes=False)
@limiter.limit("1 per minute")
def courses():
    """
    method to manage courses
		GET: returns all courses
		POST: creates a new course
    """
    if request.method == "GET":
        courses = [course.to_dict() for course in storage.all(Course).values()]
        return jsonify(courses)
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if data:
            new_course = {}
            if "code" not in data:
                abort(400, "code missing")
            new_course["code"] = data["code"]
            if "title" not in data:
                abort(400, "title  missing")
            new_course["title"] = data["title"]
            if "coeff" not in data:
                abort(400, "coeff missing")
            new_course["coeff"] = data["coeff"]
            if "teacher_id" not in data:
                abort(400, "teacher_id missing")
            if "class_id" not in data:
                abort(400, "class_id missing")
            
            # check if its a valid teacher_id
            valid_class_keys = storage.all("Teacher").keys()
            valid_class_ids = [item.split(".")[1] for item in valid_class_keys]
            if data["teacher_id"] not in valid_class_ids:
                abort(400, "teacher_id doesn't reference a valid teacher instance")
            new_course["teacher_id"] = data["teacher_id"]
            
            
            # check if its a valid class_id
            valid_class_keys = storage.all("Class").values()
            valid_class_ids = [item.code for item in valid_class_keys]
            print(valid_class_ids)
            if data["class_id"] not in valid_class_ids:
                abort(400, "class_id doesn't reference a valid class")
            new_course["class_id"] = data["class_id"]
            
            course = Course(**new_course)
            course.save()
            return jsonify(course.to_dict()), 201
    

        
            
@app_views.route("/course/<course_id>",  methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_course(course_id):
    """
    method to manage course by  ID
		GET: get a course by their ID
		DELETE: delete a course by their ID
  		UPDATE: updates an existing course with ID
    """
    course = storage.get(Course, course_id)
    if course is None:
        abort(404)
    if request.method == "GET":
        return jsonify(course.to_dict())
    
    elif request.method == "DELETE":
        storage.delete(course)
        storage.save()
        return {}, 200

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(404, "Not a JSON")
        for attribute, value in data.items():
            if attribute not in ['id', 'created_at', 'updated_at']:
                setattr(course, attribute, value)
        course.save()
        return jsonify(course.to_dict()), 201

@app_views.route("/course/<course_id>/students", methods=['GET'], strict_slashes=False)
def get_students_of_course(course_id):
    """
    method to manage admins
		GET: returns all students for a given course_id
		POST: creates a new admin
    """
    if request.method == "GET":
        course = storage.get(Course, course_id)
        
        session = storage.get_session()
        if course is None:
            course = session.query(Course).filter_by(code=course_id).first()
            if course is None:
                abort(404)
        from models.student import Student
        students = session.query(Student).join(Student.courses).filter(Course.code == course_id).all()
        student_list = [student.to_dict() for student in students]
        return student_list



@app_views.route("/course/info/<course_id>",  methods=['GET'], strict_slashes=False)
def get_course_info(course_id):
    """
    method to retrieve all information about a course
		GET: gets all information related to a course
    """
    import requests
    course_info = {}
    
    # section to manage personal information
    session = storage.get_session()
    course = storage.get(Course, course_id)
    if course is None:
            course = session.query(Course).filter_by(code=course_id).first()
            if course is None:
                abort(404)
    
    # course information
    course_details = {}
    course_info = {}
    course_info["code"] = course.code
    course_info["title"] = course.title
    course_info["coeff"] = course.coeff
    course_info["teacher_id"] = course.teacher_id
    course_info["class_id"] = course.class_id
    
    # course students
    course_details["students_list"] = get_students_of_course(course_id)
    
    # course evaluation
    student_evaluation = {}
    course_details["student_evaluation"] = get_student_evaluation(course_id)
   
    
   
    course_details["course_info"] = course_info
    return jsonify(course_details), 200

    #return jsonify(course_info), 200

@app_views.route("/course/results/<course_id>", methods=['GET'], strict_slashes=False)
def get_course_evaluation(course_id):
    """
    Method to get the evaluation results for all students in the course with course_id
    """
    from models.student import student_course
    # define a list to hold all the results
    
    course_results = []
    # the dictionary will contain dictionary of results for each student

    # get the list of students for that course
    student_list = get_students_of_course(course_id)
    student_ids  = [student["registration_number"] for student in student_list]
    
    student_result = {}
    for student in student_list:
        student_result["registration_number"] = student["registration_number"]
        student_result["first_name"] = student["first_name"]
        student_result["last_name"] = student["last_name"]
        record = session.query(student_course).filter((student_course.c.course_id == course_id) & (student_course.c.student_id == student["registration_number"])).first()
        student_result["first_term"] = [record[2], record[3], (record[2] + record[3])/2, make_remark((record[2] + record[3])/2)]
        student_result["second_term"] = [record[4], record[5], (record[4] + record[5])/2, make_remark((record[4] + record[5])/2)]
        student_result["third_term"] = [record[4], record[7], (record[6] + record[7])/2, make_remark((record[6] + record[7])/2)]
        course_results.append(student_result.copy())
    return course_results

