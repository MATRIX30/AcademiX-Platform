#!/usr/bin/python3
"""API handler for admins"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.admin import Admin
from api.v1.views import limiter

session = storage.get_session()

@app_views.route("/admins", methods=['GET', 'POST'], strict_slashes=False)
@limiter.limit("1 per minute")
def admins():
    """
    method to manage admins
		GET: returns all admins
		POST: creates a new admin
    """
    if request.method == "GET":
        admins = [admin.to_dict() for admin in storage.all(Admin).values()]
        return jsonify(admins)
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if data:
            new_admin = {}
            if "first_name" not in data:
                abort(400, "first_name missing")
            new_admin["first_name"] = data["first_name"]
            if "last_name" not in data:
                abort(400, "last_name missing")
            new_admin["last_name"] = data["last_name"]
            if "email" not in data:
                abort(400, "email missing")
            new_admin["email"] = data["email"]
            if "password" not in data:
                abort(400, "password missing")
            new_admin["password"] = data["password"]
            if "admin_type" not in data:
                abort(400, "admin_type missing")
            new_admin["admin_type"] = data["admin_type"]
            if "status" not in data:
                abort(400, "status missing")
            if not isinstance(data["status"], int):
                abort(400, "status must be int 0-inactive 1-active")
            new_admin["status"] = data["status"]
            admin = Admin(**new_admin)
            admin.save()
            return jsonify(admin.to_dict()), 201
    

        
            
@app_views.route("/admin/<admin_id>",  methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_admin(admin_id):
    """
    method to manage admin by  ID
		GET: get a admin by their ID
		DELETE: delete a admin by their ID
  		UPDATE: updates an existing admin with ID
    """
    admin = storage.get(Admin, admin_id)
    if admin is None:
        abort(404)
    if request.method == "GET":
        return jsonify(admin.to_dict())
    
    elif request.method == "DELETE":
        storage.delete(admin)
        storage.save()
        return {}, 200

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(404, "Not a JSON")
        for attribute, value in data.items():
            if attribute not in ['id', 'created_at', 'updated_at']:
                setattr(admin, attribute, value)
        admin.save()
        return jsonify(admin.to_dict()), 201


@app_views.route("/admin/info/<admin_id>",  methods=['GET'], strict_slashes=False)
def get_admin_info(admin_id):
    """
    method to retrieve all information about an admin
		GET: gets all information related to an admin
    """
    import requests
    admin_details = {}
    
    # section to manage personal information

    admin = storage.get(Admin, admin_id)
    if admin is None:
            admin = session.query(Admin).filter_by(matricule=admin_id).first()
            if admin is None:
                abort(404)
    admin_info = {}
    admin_info["status"] = admin.status
    admin_info["admin_type"] = admin.admin_type
    admin_info["created_at"] = admin.created_at
    admin_info["updated_at"] = admin.updated_at

    admin_details["admin_info"] = admin_info
  
    #from models.personnel import Personnel
    # personnel = session.query(Personnel).filter_by(id=admin["id"]).first()
    personnel = admin.personnel

    personal_info = {}
    personal_info["First_Name"] = personnel.first_name
    personal_info["Last_Name"] = personnel.last_name
    personal_info["Email"] = personnel.email
    personal_info["id"] = personnel.id
    personal_info["user_type"] = admin.__class__.__name__
    
    admin_details["personal_info"] = personal_info
    
    from models.course import Course
    from models.class_ import Class
    from models.personnel import Personnel
    from models.teacher import Teacher
    from models.student import Student

    adminstrative_info = {}
    adminstrative_info["courses"] = session.query(Course).count()
    adminstrative_info["classes"] = session.query(Class).count()
    adminstrative_info["Personnels"] = session.query(Personnel).count()
    adminstrative_info["Teachers"] = session.query(Teacher).count()
    adminstrative_info["students"] = session.query(Student).count()
    
    admin_details["adminstrative_info"] = adminstrative_info 

    
    return jsonify(admin_details), 200