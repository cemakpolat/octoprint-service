"""
@author: Cem Akpolat
@created by cemakpolat at 2020-07-24
"""

import json, logging
import docker_manager
from flask import Blueprint, request, jsonify

dockerbp = Blueprint('dockerapi', __name__)

logger = logging.getLogger()


@dockerbp.route('/dockers/names', methods=["GET", "POST"])
def get_printers():
    res = docker_manager.list_containers("octoprint")  # return only octoprint related containers
    return jsonify({"message": res, "type": "success"})
    # return json.dumps({"result": res})


@dockerbp.route('/docker/status', methods=["GET", "POST"])
def get_printer_status():
    container_name = request.values.get('printerid')
    if container_name:
        res = docker_manager.gather_container_stats(container_name)
        return jsonify({"message":res, "type": "success"})
    else:
        logger.info("Container name is not given as a parameter")
        return  jsonify({"message": "Container name is missing", "type": "error"})


@dockerbp.route('/docker/stop', methods=["GET", "POST"])
def deactivate_printer():
    container_name = request.values.get('printerid')
    if container_name:
        docker_manager.stop_container(container_name)
        res = docker_manager.list_running_containers(container_name)
        if len(res) == 0:
            #return json.dumps("{result: 'printer is stopped'}")
            return jsonify({"message": "Printer is stopped", "type": "success"})
    else:
        logger.log("container name is not given as a parameter")
        return jsonify({"message": "Container name is missing", "type": "error"})


@dockerbp.route('/docker/start', methods=["GET", "POST"])
def start_printer():
    container_name = request.values.get('printerid')
    if container_name:
        docker_manager.start_container(container_name)
        res = docker_manager.list_running_containers(container_name)
        if len(res) == 1:
            return jsonify({"message": "Printer is started","type":"success" })
    else:
        logger.debug("container name is not given as a parameter")
        return jsonify({"message": "Container name is missing","type":"error"})


@dockerbp.route('/dockers/start', methods=["GET", "POST"])
def start_all_printers():
    number = request.values.get('printerCount')
    if number.isdigit():
        docker_manager.start_printers(number)
        return jsonify({"message": "true", "type": "success"})  # json.dumps({'result': True})
    else:
        return jsonify({"message": "Printer number is not given","type":"error"}) #json.dumps({'result': "number is not given"})


@dockerbp.route('/dockers/stop', methods=["GET", "POST"])
def stop_all_printers():
    docker_manager.stop_printers()
    return jsonify({"message": "true","type":"success"}) #json.dumps({'result': True})


@dockerbp.route('/dockers/details', methods=["GET", "POST"])
def get_printer_ports():
    # return a list of printer ports and names
    result = docker_manager.get_containers_details("octoprint")
    return jsonify({"message": result,"type":"success"})


@dockerbp.route('/dockers/status', methods=["GET", "POST"])
def get_all_status_printers():
    stats = docker_manager.get_all_container_stats()
    return jsonify({"message": stats,"type":"success"})

