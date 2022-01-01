"""
@author: Cem Akpolat
@created by cemakpolat at 2021-12-29
"""

import json, logging
from flask import Blueprint, request, jsonify
import util
userapi = Blueprint('userapi', __name__)

logger = util.get_logger()


@userapi.route('/user/preferences', methods=["GET", "POST"])
def assign_user_preferences():
    profile = request.form.to_dict()
    if profile:
        #return json.dumps("{result: 'ok'}")
        return jsonify({"message": "User data is stored", "type": "success"})
    else:
        #res = "{result:'error'}"
        return jsonify({"message": "User data could not be stored", "type": "error"})
        #return json.dumps(res)
