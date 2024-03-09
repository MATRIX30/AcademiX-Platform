#!/usr/bin/python3
"""Main Handle for variour api request"""
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
def make_remark(average_score, Total=20):
    """
    This method makes a remark based on the average_score obtained
    for a given Total score the remark scheme is as follows
    Remark:
        80% and above: Excellent
        65% to 79%: Very Good
        55% to 64%: Good
        50% to 54%: Fair
        0% to 49%: Poor
    """
    score_percent = (average_score/Total)
    
    if score_percent >= 0.8:
        return "Excellent"
    elif score_percent >= 0.65:
        return "Very Good"
    elif score_percent >= 0.55:
        return "Good"
    elif score_percent >= 0.5:
        return "Fair"
    else:
        return "Poor"

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app_views,
    default_limits=["20 per day", "4 per hour"]
    )
from api.v1.views.index import *
from api.v1.views.personnels import *
from api.v1.views.admins import *
from api.v1.views.classes import *
from api.v1.views.students import *
from api.v1.views.courses import *
from api.v1.views.teachers import *
#from api.v1.views.student_course import *
