
import docker_interface
import logging

import threading
import time
import requests
import strategy

assets_in_printing_list = []
observer_running = True


def get_status_of_printer(printer):
    """
    This function retrieves the data from the given ip and port number. IP is currently not used.
    :param printer:
    :return:
    """
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


def add_to_asset_list(products):
    """
    1. get all port numbers from docker-interface
    2. call the java api for each port to see whether the printer is running or not
    3. create a list of available printers
    4. choose randomly one of the printers
    5. future task: based on the printer features, take different decisions.
    """
    if len(products) > 0:
        for product in products:

            item = {
                "name": product,
                "assignedPrinterName": "",
                "status": "waiting"
            }

            assets_in_printing_list.append(item)
        return True
    else:
        logging.warning("No product is added, since the product list empty!")
    return False


def assign_printer(products, printers):
    for product in products:
        if len(printers) > 0 and product["status"] == "waiting":
            # TODO: Selection strategy can be applied at that point
            sprinter = strategy.select_randomly(printers)
            product["assignedPrinterName"] = sprinter["name"]
            product["status"] = "printing"
            printers.remove(sprinter)


class PrinterObserver(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        # estimated printing duration is not involved in the system.
        while observer_running:

            if len(assets_in_printing_list) > 0:
                printers = docker_interface.get_containers_details("octoprint")

                non_occupied_printers = []

                for printer in printers:
                    if is_printer_free(printer):
                        non_occupied_printers.append(printer)

                # filter the completed works
                for printer in non_occupied_printers:
                    for item in assets_in_printing_list:
                        if item["assignedPrinterName"] == printer["name"]:
                            assets_in_printing_list.remove(item)

                assign_printer(assets_in_printing_list, non_occupied_printers)

            else:
                time.sleep(5)

            time.sleep(5)
        logging.info("Printer observer is stopping...")
        return


def start_observer():
    t = PrinterObserver(args=(), kwargs={'test':'data'})
    t.start()
    logging.info("Printer observer is started..")


def stop_observer():
    global observer_running
    observer_running = False
    logging.info("Printer observer is stopped ..")


class PrinterOwner:
    """
    The purpose of this class is to select the best option that can be used
    In the future, other parameters should be also involved here to make the decision harder
    The printer owners would have different devices, quality, delivery time as well as cost
    The decision will be based on those parameters.
    """
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
        self.creator = "Beagle Bone"
        self.complexity = "100"  # 0-100
