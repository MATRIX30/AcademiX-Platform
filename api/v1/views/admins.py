#!/usr/bin/python3
"""API handler for admins"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.admin import Admin
from api.v1.views import limiter



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
                abort(400, "status missing")
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
