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


# call rest of the java app
# see the printer is not printing
# select randomly the printer

def get_status_of_printer(printer):
    printer_data = ""
    return printer_data


def is_printer_free(printer):
    return True


def selectPrinter(strategy="random"):
    """
    1. get all port numbers from docker-interface
    2. call the java api for each port to see whether the printer is running or not
    3. create a list of available printers
    4. choose randomly one of the printers
    5. future task: based on the printer features, take different decisions.
    """
    print("selected printer into")
    selected_printer = None
    printers = docker_interface.get_containers_details("octoprint")

    non_occupied_printers = []
    print("printers", printers)

    for printer in printers:
        if is_printer_free(printer):
            non_occupied_printers.append(printer)
        print(printer)

    if strategy == "random":
        selected_printer = select_randomly(non_occupied_printers)

    logging.info("Selected printer: ", selected_printer)
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
