"""
@author: Cem Akpolat
@created by cemakpolat at 2020-07-24
"""

import os, json
from flask import jsonify, Blueprint, request
from werkzeug.utils import secure_filename
import assets_manager

assetsapi = Blueprint('assetsapi', __name__)


UPLOAD_FOLDER = '../models'
ALLOWED_EXTENSIONS = set(['gcode'])


@assetsapi.route('/models', methods=["GET", "POST"])
def get_all_models():
    flist = assets_manager.get_printable_models()
    return jsonify({'message': flist})
    # return json.dumps({"result": flist})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@assetsapi.route('/printers/assets/upload', methods=["GET", "POST"])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 206
        return resp
    if success:
        resp = jsonify({'message': 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp

