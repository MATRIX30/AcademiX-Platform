#!/usr/bin/python3
"""Main Handle for variour api request"""
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app_views,
    default_limits=["20 per day", "4 per hour"]
    )
from api.v1.views.index import *
from api.v1.views.personnels import *
# from api.v1.views.admins import *
# from api.v1.views.classes import *
# from api.v1.views.students import *
# from api.v1.views.courses import *
