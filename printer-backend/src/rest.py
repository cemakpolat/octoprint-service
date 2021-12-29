# import logging, json, os
# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS, cross_origin
# import docker_manager, util, printer_decision, assets_manager
# from werkzeug.utils import secure_filename
#
#
# logger = logging.getLogger()
#
# app = Flask(__name__)
# CORS(app, support_credentials=True)
#
#
# # Printer control
#
#
# @app.route('/dockers/names', methods=["GET", "POST"])
# def get_printers():
#     res = docker_manager.list_containers("octoprint")  # return only octoprint related containers
#
#     return json.dumps({"result": res})
#
#
# @app.route('/docker/status', methods=["GET", "POST"])
# def get_printer_status():
#     container_name = request.values.get('printerid')
#     if container_name:
#         res = docker_manager.gather_container_stats(container_name)
#     else:
#         res = "{}"
#         logger.log("container name is not given as a parameter")
#     return json.dumps(res)
#
#
# @app.route('/docker/stop', methods=["GET", "POST"])
# def deactivate_printer():
#     container_name = request.values.get('printerid')
#     if container_name:
#         docker_manager.stop_container(container_name)
#         res = docker_manager.list_running_containers(container_name)
#         print(res)
#         if len(res) == 0:
#             return json.dumps("{result: 'printer is stopped'}")
#     else:
#         res = "{error:'Container name is missing'}"
#         logger.log("container name is not given as a parameter")
#     return json.dumps(res)
#
#
# @app.route('/docker/start', methods=["GET", "POST"])
# def start_printer():
#     container_name = request.values.get('printerid')
#     if container_name:
#         docker_manager.start_container(container_name)
#         res = docker_manager.list_running_containers(container_name)
#         print(res)
#         if len(res) == 1:
#             return json.dumps("{result: 'Printer is started'}")
#     else:
#         res = "{error:'Container name is missing'}"
#         logger.log("container name is not given as a parameter")
#     return json.dumps(res)
#
#
# @app.route('/user/preferences', methods=["GET", "POST"])
# def assign_user_preferences():
#     profile = request.form.to_dict()
#     if profile:
#         return json.dumps("{result: 'ok'}")
#     else:
#         res = "{result:'error'}"
#     return json.dumps(res)
#
#
# @app.route('/dockers/start', methods=["GET", "POST"])
# def start_all_printers():
#     number = request.values.get('printerCount')
#     print(number)
#     if number.isdigit():
#         docker_manager.start_printers(number)
#     else:
#         return json.dumps({'result': "number is not given"})
#     return json.dumps({'result': True})
#
#
# @app.route('/dockers/stop', methods=["GET", "POST"])
# def stop_all_printers():
#     docker_manager.stop_printers()
#     return json.dumps({'result': True})
#
#
# @app.route('/dockers/details', methods=["GET", "POST"])
# def get_printer_ports():
#     # return a list of printer ports and names
#     result = docker_manager.get_containers_details("octoprint")
#     return json.dumps({"result": result})
#
#
# @app.route('/dockers/status', methods=["GET", "POST"])
# def get_all_status_printers():
#     stats = docker_manager.get_all_container_stats()
#     return json.dumps({"result": stats})
#
#
# # Printer Decision
#
# @app.route('/printers/select', methods=["GET", "POST"])
# def assign_printer():
#     product_list = request.form.getlist('products[]')
#     # print("Assets to be printed:", product_list)
#
#     if product_list and printer_decision.add_to_asset_list(product_list):
#         res = "The {products} are added to the list".format(products=str(product_list))
#     else:
#         res = "The product list is empty!"
#         logger.warning("container name is not given as a parameter")
#
#     return json.dumps({"result": res})
#
#
# @app.route('/printers/assets/status', methods=["GET", "POST"])
# def get_ordered_asset_statuses():
#     return jsonify(printer_decision.assets_in_printing_list);
#
#
# # Assets manager
# # Interacting with Printable Models
#
# @app.route('/models', methods=["GET", "POST"])
# def get_all_models():
#     flist = assets_manager.get_printable_models()
#     return json.dumps({"result": flist})
#
#
# UPLOAD_FOLDER = '../models'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = set(['gcode'])
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# @app.route('/printers/assets/upload', methods=["GET", "POST"])
# def upload_file():
#     # check if the post request has the file part
#     if 'files[]' not in request.files:
#         resp = jsonify({'message': 'No file part in the request'})
#         resp.status_code = 400
#         return resp
#
#     files = request.files.getlist('files[]')
#
#     errors = {}
#     success = False
#
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             success = True
#         else:
#             errors[file.filename] = 'File type is not allowed'
#
#     if success and errors:
#         errors['message'] = 'File(s) successfully uploaded'
#         resp = jsonify(errors)
#         resp.status_code = 206
#         return resp
#     if success:
#         resp = jsonify({'message': 'Files successfully uploaded'})
#         resp.status_code = 201
#         return resp
#     else:
#         resp = jsonify(errors)
#         resp.status_code = 400
#         return resp
#
#
# @app.route('/printers/assets', methods=["GET", "POST"])
# def get_assets_in_printing_process():
#     return json.dumps({"result": printer_decision.assets_in_printing_list})
#
#
# if __name__ == '__main__':
#     docker_manager.start_printers(1)
#     printer_decision.start_observer()
#     app.run(host='0.0.0.0', port='8001', debug=False)
