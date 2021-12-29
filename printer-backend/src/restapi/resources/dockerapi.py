"""
@author: Cem Akpolat
@created by cemakpolat at 2020-07-24
"""

import json, logging
import docker_manager
from flask import Blueprint, request

dockerbp = Blueprint('dockerapi', __name__)

logger = logging.getLogger()


@dockerbp.route('/dockers/names', methods=["GET", "POST"])
def get_printers():
    res = docker_manager.list_containers("octoprint")  # return only octoprint related containers

    return json.dumps({"result": res})


@dockerbp.route('/docker/status', methods=["GET", "POST"])
def get_printer_status():
    container_name = request.values.get('printerid')
    if container_name:
        res = docker_manager.gather_container_stats(container_name)
    else:
        res = "{}"
        logger.log("container name is not given as a parameter")
    return json.dumps(res)


@dockerbp.route('/docker/stop', methods=["GET", "POST"])
def deactivate_printer():
    container_name = request.values.get('printerid')
    if container_name:
        docker_manager.stop_container(container_name)
        res = docker_manager.list_running_containers(container_name)
        print(res)
        if len(res) == 0:
            return json.dumps("{result: 'printer is stopped'}")
    else:
        res = "{error:'Container name is missing'}"
        logger.log("container name is not given as a parameter")
    return json.dumps(res)


@dockerbp.route('/docker/start', methods=["GET", "POST"])
def start_printer():
    container_name = request.values.get('printerid')
    if container_name:
        docker_manager.start_container(container_name)
        res = docker_manager.list_running_containers(container_name)
        print(res)
        if len(res) == 1:
            return json.dumps("{result: 'Printer is started'}")
    else:
        res = "{error:'Container name is missing'}"
        logger.log("container name is not given as a parameter")
    return json.dumps(res)


@dockerbp.route('/dockers/start', methods=["GET", "POST"])
def start_all_printers():
    number = request.values.get('printerCount')
    print(number)
    if number.isdigit():
        docker_manager.start_printers(number)
    else:
        return json.dumps({'result': "number is not given"})
    return json.dumps({'result': True})


@dockerbp.route('/dockers/stop', methods=["GET", "POST"])
def stop_all_printers():
    docker_manager.stop_printers()
    return json.dumps({'result': True})


@dockerbp.route('/dockers/details', methods=["GET", "POST"])
def get_printer_ports():
    # return a list of printer ports and names
    result = docker_manager.get_containers_details("octoprint")
    return json.dumps({"result": result})


@dockerbp.route('/dockers/status', methods=["GET", "POST"])
def get_all_status_printers():
    stats = docker_manager.get_all_container_stats()
    return json.dumps({"result": stats})

