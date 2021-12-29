"""
@author: Cem Akpolat
@created by cemakpolat at 2021-12-29
"""

import json, logging
from flask import Blueprint, request

userapi = Blueprint('userapi', __name__)

logger = logging.getLogger()


@userapi.route('/user/preferences', methods=["GET", "POST"])
def assign_user_preferences():
    profile = request.form.to_dict()
    if profile:
        return json.dumps("{result: 'ok'}")
    else:
        res = "{result:'error'}"
    return json.dumps(res)