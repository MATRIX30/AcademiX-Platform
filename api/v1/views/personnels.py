#!/usr/bin/python3
"""API handler for Personnels"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.personnel import Personnel
from api.v1.views import limiter



@app_views.route("/personnels", methods=['GET', 'POST'], strict_slashes=False)
@limiter.limit("1 per minute")
def personnels():
    """
    method to manage personnels
		GET: returns all personnels
		POST: creates a new personnel
    """
    if request.method == "GET":
        personnels = [personnel.to_dict() for personnel in storage.all(Personnel).values()]
        return jsonify(personnels)
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(400, "Not a JSON")
        if data:
            new_personnel = {}
            if "first_name" not in data:
                abort(400, "first_name missing")
            new_personnel["first_name"] = data["first_name"]
            if "last_name" not in data:
                abort(400, "last_name missing")
            new_personnel["last_name"] = data["last_name"]
            if "email" not in data:
                abort(400, "email missing")
            new_personnel["email"] = data["email"]
            if "password" not in data:
                abort(400, "password missing")
            new_personnel["password"] = data["password"]
            
            personnel = Personnel(**new_personnel)
            personnel.save()
            return jsonify(personnel.to_dict()), 201
    

        
            
@app_views.route("/personnel/<personnel_id>",  methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_personnel(personnel_id):
    """
    method to manage personnel by  ID
		GET: get a personnel by their ID
		DELETE: delete a personnel by their ID
  		UPDATE: updates an existing personnel with ID
    """
    personnel = storage.get(Personnel, personnel_id)
    if personnel is None:
        abort(404)
    if request.method == "GET":
        return jsonify(personnel.to_dict())
    
    elif request.method == "DELETE":
        storage.delete(personnel)
        storage.save()
        return {}, 200

    elif request.method == "PUT":
        data = request.get_json(silent=True)
        if data is None or not isinstance(data, dict):
            abort(404, "Not a JSON")
        for attribute, value in data.items():
            if attribute not in ['id', 'created_at', 'updated_at']:
                setattr(personnel, attribute, value)
        personnel.save()
        return jsonify(personnel.to_dict()), 201
