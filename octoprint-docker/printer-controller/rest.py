import logging, json
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import docker_interface, util, printer_decision, printable_models

logger = logging.getLogger()
app = Flask(__name__)
CORS(app, support_credentials=True)

# Printer control
@app.route('/', methods=["GET", "POST"])
def hello():
    return "hello world"


@app.route('/printers', methods=["GET", "POST"])
def get_printers():
    res = docker_interface.list_containers("octoprint")  # return only octoprint related containers
    return json.dumps({"result":res})


@app.route('/printer/status', methods=["GET", "POST"])
def get_printer_status():
    container_name = request.values.get('printerid')
    if container_name:
        res = docker_interface.gather_container_stats(container_name)
    else:
        res = "{}"
        logger.log("container name is not given as a parameter")
    return json.dumps(res)


@app.route('/printer/stop', methods=["GET", "POST"])
def deactivate_printer():
    container_name = request.values.get('printerid')
    if container_name:
        docker_interface.stop_container(container_name)
        res = docker_interface.list_containers(container_name)
        print(res)
        if len(res) == 0:
            return json.dumps("{result: 'printer is stopped'}")
    else:
        res = "{error:'Container name is missing'}"
        logger.log("container name is not given as a parameter")
    return json.dumps(res)


@app.route('/printer/start', methods=["GET", "POST"])
def start_printer():
    container_name = request.values.get('printerid')
    if container_name:
        docker_interface.start_container(container_name)
        res = docker_interface.list_containers(container_name)
        print(res)
        if len(res) == 1:
            return json.dumps("{result: 'Printer is started'}")
    else:
        res = "{error:'Contaier name is missing'}"
        logger.log("container name is not given as a parameter")
    return json.dumps(res)


@app.route('/printers/start', methods=["GET", "POST"])
def start_all_printers():
    number = request.values.get('printerCount')
    docker_interface.start_printers(number)
    return json.dumps({'result': True})


@app.route('/printers/stop', methods=["GET", "POST"])
def stop_all_printers():
    docker_interface.stop_printers()
    return json.dumps({'result': True})


@app.route('/printers/details', methods=["GET", "POST"])
def get_printer_ports():
    # return a list of printer ports and names
    result = docker_interface.get_containers_details("octoprint")
    return json.dumps({"result":result})


@app.route('/printers/status', methods=["GET", "POST"])
def get_all_status_printers():
    stats = docker_interface.get_all_container_stats()
    return json.dumps({"result":stats})


#### Interacting with Printable Models

@app.route('/models', methods=["GET", "POST"])
def get_all_models():
    flist = printable_models.get_printable_models()
    return json.dumps({"result": flist})


#### Printer Decision

@app.route('/printers/select', methods=["GET", "POST"])
def get_decided_printer():
    selected_printer = printer_decision.selectPrinter()
    return json.dumps({"result":selected_printer})


if __name__ == '__main__':
    docker_interface.start_printers(1)
    app.run(host='0.0.0.0', port='8001', debug=True)