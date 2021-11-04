import subprocess, logging, socket, json, os
import util
import docker


# start all printers with a number
def start_printers(number):
    import os
    # data = {}
    # data['printer-dockers'] = []

    plist = util.get_available_port_numbers(number)

    for i in range(len(plist)):
        with open("../docker-compose.yml_backup", "rt") as fin:
            with open("../docker-compose.yml", "wt") as fout:
                for line in fin:
                    fout.write(line.replace('${port}', plist[i]))

        stream = os.popen('docker-compose -f ../docker-compose.yml -p appv' + str(i) + ' up -d')
        output = stream.read()
        print(output)
    #     data['printer-dockers'].append({
    #         'port': plist[i],
    #         'name': 'appv' + str(i) +"_octoprint_1"
    #     })
    # util.write_to_file(data)


# stop all printers dockers
def stop_printers():
    containers = list_containers("octoprint")
    for item in containers:
        stop_container(item)


# start a single already composed container
def start_container(package):
    if is_container_available(package):
        print("container is available")
    client = get_docker_client()
    container = client.containers.get(package)
    container.start()
    return container


# stop a single container
def stop_container(printer_id):
    client = get_docker_client()
    container = client.containers.get(printer_id)
    container.stop()


# get docker client
def get_docker_client():
    client = docker.from_env()
    return client


# get all container status
def get_all_container_stats():

    stats = []
    clist = list_containers("octoprint")
    for cnt in clist:
        stats.append(gather_container_stats(cnt))
    return stats

# get docker statistics
def gather_container_stats(container_name):

    """
    Used to gather the execution stats for a Docker Container by its ID
    name, cpu, mem usae, net io,

    :param container_id:
    :return:
    """
    docker_url = "unix://var/run/docker.sock"
    api_client = docker.APIClient(base_url=docker_url)
    cid = get_container_id(container_name)
    if cid:
        res = api_client.stats(container=cid, stream=False)
        print(res)
        # send only few data, not all
        """
        
        """
        res = {"name":res["name"],"cpu":res["cpu_stats"]["cpu_usage"]["total_usage"],"mem":res["memory_stats"]["usage"],"net":{
            "ingress":res["networks"]["eth0"]["rx_bytes"],
            "egress":res["networks"]["eth0"]["tx_bytes"]
        }}
    else:
        logging.warning("Container ID does not exist!")
        res = "{}"
    return res


# get container id
def get_container_id(cname):
    client = get_docker_client()
    containers = client.containers.list()
    for container in containers:
        if cname == container.name:
            return container.short_id
    return None


# list all running containers
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

# list all containers with the given name
def list_containers(search_tag):
    client = get_docker_client()
    containers = client.containers.list()
    result = []
    for container in containers:
        if search_tag in container.name:
            result.append(container.name)
    return result


def get_containers_details(search_tag):
    """
        {
    [{
    name:"dockertests-name",
    "ip":"ip",
    "port":"port",
    "status":"running"
    }]
    }

    :param search_tag:
    :return:
    """
    client = get_docker_client()
    containers = client.containers.list()
    result = []
    for container in containers:
        #print(container.attrs)
        if search_tag in container.name:
            result.append({"name":container.name,"port":container.attrs['HostConfig']['PortBindings']['5000/tcp'][0]['HostPort'], "status":container.status,"ip":container.attrs['HostConfig']['PortBindings']['5000/tcp'][0]['HostIp']})
    return result


# check whether the container is available
def is_container_available(package_name):
    result = False
    client = get_docker_client()
    containers = client.containers.list(all=True)
    for container in containers:
        if container.name == package_name:
            result = True
    return result


# delete container with the given id
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
