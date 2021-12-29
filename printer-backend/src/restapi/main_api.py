"""
@author: Cem Akpolat
@created by cemakpolat at 2020-07-24
"""
from flask import Flask
from restapi.resources import assetsapi, dockerapi, printingapi, userapi
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

UPLOAD_FOLDER = '../models'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['gcode'])

api_version = "" #"/api/v1"

app.register_blueprint(assetsapi.assetsapi, url_prefix=api_version)
app.register_blueprint(dockerapi.dockerbp, url_prefix=api_version)
app.register_blueprint(printingapi.printingapi, url_prefix=api_version)
app.register_blueprint(userapi.userapi, url_prefix=api_version)


def run():
    app.run(host='0.0.0.0', port='8001', debug=False)
