#!/usr/bin/python3
"""API handler for admins"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.student import student_course

from sqlalchemy import update

session = storage.get_session()



@app_views.route("/student_course", methods=['POST'], strict_slashes=False)
def student_results():
    """
    method to manage students
		POST: insert students and marks for a course to student_course table
    """
    if request.method == "POST":
        data = request.get_json(silent=True)
        print(data)
        if data is None or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if data:
            new_student_course = {}
            if "course_id" not in data:
                abort(400, "course_id missing")
            new_student_course["course_id"] = data["course_id"]
            if "student_id" not in data:
                abort(400, "student_id missing")
            new_student_course["student_id"] = data["student_id"]
            
            if "term" not in data:
                abort(400, "term missing")
            new_student_course["term"] = data["term"]
            
            if "first_mark" not in data:
                abort(400, "first_mark missing")
            new_student_course["first_mark"] = data["first_mark"]
            if "second_mark" not in data:
                abort(400, "second_mark missing")
            new_student_course["second_mark"] = data["second_mark"]
            
            # Update function specifying the table and update condition
            
            if data["term"] == 1: 
                update_stmt = (
                    update(student_course).where(student_course.c.student_id == new_student_course["student_id"] )
                    .where(student_course.c.course_id == new_student_course["course_id"])
                    .values(first_seq=new_student_course["first_mark"], second_seq=new_student_course["second_mark"])
                )
                # Execute the update statement
                session.execute(update_stmt)
            if data["term"] == 2:
                update_stmt = (
                    update(student_course).where(student_course.c.student_id == new_student_course["student_id"] )
                    .where(student_course.c.course_id == new_student_course["course_id"])
                    .values(third_seq=new_student_course["first_mark"],fourth_seq=new_student_course["second_mark"])
                )
                # Execute the update statement
                session.execute(update_stmt)
            if data["term"] == 3:
                update_stmt = (
                    update(student_course).where(student_course.c.student_id == new_student_course["student_id"] )
                    .where(student_course.c.course_id == new_student_course["course_id"])
                    .values(fifth_seq=new_student_course["first_mark"], sixth_seq=new_student_course["second_mark"])
                )
                # Execute the update statement
                session.execute(update_stmt)

            session.commit()
        return jsonify({"msg":"successful"}), 201
