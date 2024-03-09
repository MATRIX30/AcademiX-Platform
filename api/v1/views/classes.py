#!/usr/bin/python3
"""API handler for Classs"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.class_ import Class
from api.v1.views import limiter



@app_views.route("/classes", methods=['GET', 'POST'], strict_slashes=False)
@limiter.limit("1 per minute")
def classs():
    """
    method to manage classs
		GET: returns all classes
		POST: creates a new class
    """
    if request.method == "GET":
        classes = [class_.to_dict() for class_ in storage.all(Class).values()]
        return jsonify(classes)
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if data:
            new_class = {}
            if "name" not in data:
                abort(400, "name missing")
            new_class["name"] = data["name"]
            if "code" not in data:
                abort(400, "code missing")
            new_class["code"] = data["code"]
            if "number_of_students" not in data:
                abort(400, "number_of_students missing")
            new_class["number_of_students"] = data["number_of_students"]
            
            if "courses"  in data:
                # abort(400, "list of course(s) ID missing")
                if not isinstance(data["courses"], list):
                    abort(400, "Wrong format: courses should be in list format eg ['CS50', 'MATH101]")
                all_courses = storage.all("Course").keys()
                course_ids = [key.split(".")[1] for key in all_courses]
                
                for id in data["courses"]:
                    if id not in  course_ids:
                        abort(400, "{} does not reference an existing course".format(id))
                new_class["courses"] = data["courses"]
            
            if "students" in data:
                # abort(400, "list of student(s) ID missing")
                if not isinstance(data["students"], list):
                    abort(400, "Wrong format: students should be in list format eg ['CS50', 'MATH101]")
                all_students = storage.all("Student").keys()
                student_ids = [key.split(".")[1] for key in all_students]
            
                for id in data["students"]:
                    if id not in  student_ids:
                        abort(400, "{} does not reference an existing student".format(id))
                new_class["students"] = data["students"]
            
            class_ = Class(**new_class)
            class_.save()
            return jsonify(class_.to_dict()), 201
    

        
            
@app_views.route("/class/<class_id>",  methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_class(class_id):
    """
    method to manage class by  ID
		GET: get a class by their ID
		DELETE: delete a class by their ID
  		UPDATE: updates an existing class with ID
    """
    class_ = storage.get(Class, class_id)
    if class_ is None:
        abort(404)
    if request.method == "GET":
        return jsonify(class_.to_dict())
    
    elif request.method == "DELETE":
        storage.delete(class_)
        storage.save()
        return {}, 200

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(404, "Not a JSON")
        for attribute, value in data.items():
            if attribute not in ['id', 'created_at', 'updated_at']:
                setattr(class_, attribute, value)
        class_.save()
        return jsonify(class_.to_dict()), 201
