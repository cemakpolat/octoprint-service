"""
The purpose of this class is to select the best option that can be used
In the future, other parameters should be also involved here to make the decision harder
The printer owners would have different devices, quality, delivery time as well as cost
The decision will be based on those parameters.

Printer-owner :{
owner:"name",
quality:"resolution",
cost:"0-100",
deliveryTime:"3",# days
possibleEnergyConsumption:"100",
climaEffect:"0", # due to the consumed energy!
device:"x-marke",
}

Printable-Product-Owner :{

}
"""
import docker_interface
import logging
import random
import requests


def get_status_of_printer(printer):
    port = {"port": printer["port"]}
    r = requests.get('http://localhost:8080/printer/status', params=port)
    return r.json()


def is_printer_free(printer):
    response = get_status_of_printer(printer)
    if response["content"] == "OPERATIONAL" or response["content"] == "READY":
        return True
    else:
        print("Printer cannot be selected since it is in the mode "+response["content"])

    return False


def selectPrinter(productList, strategy=None):
    """
    1. get all port numbers from docker-interface
    2. call the java api for each port to see whether the printer is running or not
    3. create a list of available printers
    4. choose randomly one of the printers
    5. future task: based on the printer features, take different decisions.
    """
    printers = docker_interface.get_containers_details("octoprint")

    non_occupied_printers = []

    for printer in printers:
        if is_printer_free(printer):
            non_occupied_printers.append(printer)

    print("strategy is none", strategy)
    selected_printer = select_randomly(non_occupied_printers)

    print("Selected printer: ", selected_printer)
    return selected_printer


def select_randomly(printers):
    return random.choice(printers)


class PrinterOwner:
    def __init__(self):
        self.owner = "name"
        self.quality = "resolution"
        self.cost = "0-100"
        self.deliveryTime = "3"
        self.possibleEnergyConsumption = "100"
        self.climaEffect = "0" # due to the consumed energy!
        self.device = "x-marke"


class ProductModel:
    def __init__(self):
        self.name = "name"
        self.creator = "Cem Akpolat"
        self.complexity = "100" # 0-100



#
# import threading
# import logging
# import time
#
# logging.basicConfig(level=logging.DEBUG,
#                     format='(%(threadName)-10s) %(message)s',
#                     )
# productList = [1]
# class MyThreadWithArgs(threading.Thread):
#
#     def __init__(self, group=None, target=None, name=None,
#                  args=(), kwargs=None, verbose=None):
#         threading.Thread.__init__(self, group=group, target=target, name=name)
#         self.args = args
#         self.kwargs = kwargs
#         return
#
#     def run(self):
#         while len(productList) > 0 :
#             logging.debug('running with %s and %s, size %s', self.args, self.kwargs, str(len(productList)))
#             time.sleep(3)
#
#             if len(productList) > 5:
#                 logging.debug("removing item ...")
#                 productList.pop()
#                 logging.debug("current length: %s", str(len(productList)))
#             else:
#                 productList.append("aa")
#
#         return
#
#
# for i in range(5):
#     t = MyThreadWithArgs(args=(i,), kwargs={'a':'A', 'b':'B'})
#     t.start()
# 