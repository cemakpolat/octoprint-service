"""
@author: Cem Akpolat
@created by cemakpolat at 2021-10-06
"""
import subprocess
import logging
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import socket

import json
import docker
logger = logging.getLogger()
app = Flask(__name__)
CORS(app, support_credentials=True)


# ================ get all running printers ======================
@app.route('/', methods=["GET", "POST"])
def hello():
    return "hello world"


@app.route('/printers', methods=["GET", "POST"])
def get_printers():
    res = list_containers("octoprint")  # return only octoprint related containers
    print(res)
    return json.dumps(res)


@app.route('/printer/status', methods=["GET", "POST"])
def get_printer_status():
    container_name = request.values.get('printerid')
    if container_name:
        res = gather_container_stats(container_name)
    else:
        res = "{}"
        logger.log("container name is not given as a parameter")
    return json.dumps(res)


@app.route('/printer/stop', methods=["GET", "POST"])
def deactivate_printer():
    container_name = request.values.get('printerid')
    if container_name:
        stop_container(container_name)
        res = list_containers(container_name)
        print(res)
        if len(res) == 0:
            return json.dumps("{result: 'printer is stopped'}")
    else:
        res = "{}"
        logger.log("container name is not given as a parameter")
    return json.dumps(res)


@app.route('/printer/start', methods=["GET", "POST"])
def start_printer():
    container_name = request.values.get('printerid')
    if container_name:
        start_container(container_name)
        res = list_containers(container_name)
        print(res)
        if len(res) == 1:
            return json.dumps("{result: 'printer is started'}")
    else:
        res = "{}"
        logger.log("container name is not given as a parameter")
    return json.dumps(res)


@app.route('/printers/start', methods=["GET", "POST"])
def start_all_printers():
    number = request.values.get('printerCount')
    start_printers(number)
    return json.dumps({'result': True})


@app.route('/printers/stop', methods=["GET", "POST"])
def stop_all_printers():
    stop_printers()
    return json.dumps({'result': True})


@app.route('/printers/ports', methods=["GET", "POST"])
def get_all_printer_ports():
    return read_from_file()


@app.route('/printers/status', methods=["GET", "POST"])
def get_all_status_printers():
    res = list_containers("octoprint")
    stats = []
    for item in res:
        stats.append(gather_container_stats(item))
    return json.dumps(stats)


@app.route('/printers/models', methods=["GET", "POST"])
def get_all_models():
    import os
    files = os.listdir("./models/")
    flist = []
    for f in files:
        flist.append(f)
    return json.dumps(flist)



def stop_container(printer_id):
    client = get_docker_client()
    container = client.containers.get(printer_id)
    container.stop()


def write_to_file(data):
    with open('docker-ports.txt', 'w') as outfile:
        json.dump(data, outfile)


def read_from_file():
    with open('docker-ports.txt') as json_file:
        data = json.load(json_file)
        print(data['printer-dockers'])
        return data


def start_printers(number):
    import os
    data = {}
    data['printer-dockers'] = []

    plist = get_available_port_numbers(number)

    for i in range(len(plist)):
        with open("docker-compose.yml_backup", "rt") as fin:
            with open("docker-compose.yml", "wt") as fout:
                for line in fin:
                    fout.write(line.replace('${port}', plist[i]))

        stream = os.popen('docker-compose -p appv' + str(i) + ' up -d')
        output = stream.read()
        print(output)
        data['printer-dockers'].append({
            'port': plist[i],
            'name': 'appv' + str(i) +"_octoprint_1"
        })
    write_to_file(data)


def start_container(package):
    if is_container_available(package):
        print("container is available")
    client = get_docker_client()
    container = client.containers.get(package)
    container.start()
    return container


def stop_printers():
    containers = list_containers("octoprint")
    for item in containers:
        stop_container(item)


def delete_container(container_docker_id):
    """delete container by container dockertest id"""
    client = get_docker_client()
    obj_container = client.containers.get(container_docker_id)
    obj_container.stop()
    obj_container.reload()
    if obj_container.status == 'exited':
        return True
    else:
        return False


def get_available_port_numbers(number):
    # starting point 50000
    plist = []
    i = 0
    while i < number:
        if is_port_free(int("5000"+str(i))) is True:
            plist.append("5000"+str(i))
        else:
            number = number +1
        i += 1
    return plist


def is_port_free(port):

    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        result = False
    else:
        result = True
    a_socket.close()
    return result


def get_docker_client():
    client = docker.from_env()
    return client


def gather_container_stats(container_name):

    """
    Used to gather the execution stats for a Docker Container by its ID
    :param container_id:
    :return:
    """
    docker_url = "unix://var/run/docker.sock"
    api_client = docker.APIClient(base_url=docker_url)
    cid = get_container_id(container_name)
    if cid:
        res = api_client.stats(container=cid, stream=False)
    else:
        res = "{}"
    return res


def get_container_id(cname):
    client = get_docker_client()
    containers = client.containers.list()
    for container in containers:
        if cname == container.name:
            return container.short_id
    return None


def list_running_containers():
    client = get_docker_client()
    containers = client.containers.list()

    result = []
    for container in containers:
        print(container)
        # if PACKAGE_IMAGE_NAME in container.image.tags and str(container.status) == 'running':
        if str(container.status) == 'running':
            result.append(container.name)

    return result


def list_containers(search_tag):
    client = get_docker_client()
    containers = client.containers.list()
    result = []
    for container in containers:
        print(container.attrs['State'], container.attrs['Name'], container.attrs['HostConfig']['PortBindings'])
        if search_tag in container.name:
            result.append(container.name)
    return result


def is_container_available(package_name):
    result = False
    client = get_docker_client()
    containers = client.containers.list(all=True)
    for container in containers:
        if container.name == package_name:
            result = True
    return result


def read_printable_models():
    import glob
    pfiles = []
    for file in glob.glob("*.txt"):
        pfiles.append(file)
    return pfiles


if __name__ == '__main__':
    start_printers(1)
    app.run(host='0.0.0.0', port='8000', debug=True)

