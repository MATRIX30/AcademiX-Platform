#!/usr/bin/python3
"""AcademiX API Main routes"""

from api.v1.views import app_views
from flask import jsonify
from models.personnel import Personnel
from models.admin import Admin
from models.class_ import Class
from models.teacher import Teacher
from models.course import Course
from models.student import Student
from models import storage

classes = {"Teacher": Teacher, "Course":Course,
           "Class":Class, "Personnel": Personnel, "Admin":Admin,
            "Student":Student}

@app_views.route("/status", strict_slashes=False)
def status():
    """
    method to verify status of API server
    and return json response
    """
    response = {
		"Status" : "OK"
	}
    return jsonify(response)

@app_views.route("/stats", strict_slashes=False)
def stats():
    """Endpoint to get the total number of objects of the  system"""
    stat_dic = {}
    for cls_name, cls in classes.items():
        stat_dic[cls_name] = storage.count(cls)
    return jsonify(stat_dic)
