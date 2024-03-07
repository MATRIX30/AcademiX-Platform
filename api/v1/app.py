#!/usr/bin/python3
""" Main flask app to handle AcademiX API"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_session(Exception):
    """
    method to close down the session by
    disconnecting from storage engine
    """
    storage.close()
    
@app.errorhandler(404)
def not_found(Exception):
    """Returns Not found error for a request"""
    return jsonify({"Error": "Not Found"}), Exception.code
    
if __name__ == "__main__":
    academiX_host = getenv('ACADEMIX_API_HOST')
    academiX_port = getenv('ACADEMIX_API_PORT')
    
    if not academiX_host:
        academiX_host = "0.0.0.0"
    if not academiX_port:
        academiX_port = 6000
    app.run(host=academiX_host, port=academiX_port, debug=True, threaded=True)