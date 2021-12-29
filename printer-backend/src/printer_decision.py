import logging

import threading
import time

from src import strategy, octoprint_restapi as pr, util, docker_manager

assets_in_printing_list = []
observer_running = True
printer_status_list = []


def add_to_asset_list(products):
    """
    1. get all port numbers from docker-interface
    2. call the java api for each port to see whether the printer is running or not
    3. create a list of available printers
    4. choose randomly one of the printers
    5. future task: based on the printer features, take different decisions.
    """
    global assets_in_printing_list
    if len(products) > 0:
        for product in products:
            item = {
                "name": product,
                "assignedPrinterName": "",
                "status": "waiting",
                "started": None
            }
            assets_in_printing_list.append(item)
        return True
    else:
        logging.warning("No product is added, since the product list empty!")
    return False


def remove(obj, printers):
    for item in printers:
        if item["name"] == obj["name"]:
            printers.remove(item)
            print("{item} is removed".format(item=item["name"]))


def check_printer_initiation_duration(starttime):
    """
     Wait 60 seconds for printing initiation, if it is more than this time, this means the printing is already started
    """
    difference = util.time_difference_in_sec(util.get_current_time(), starttime)
    if difference > 60:
        return True


def assign_printer(printers):
    for index in range(len(assets_in_printing_list)):
        if len(printers) > 0 and assets_in_printing_list[index]["status"] == "waiting":
            sprinter = strategy.select_randomly(printers)
            assets_in_printing_list[index]["assignedPrinterName"] = sprinter["name"]
            assets_in_printing_list[index]["status"] = "printing"
            assets_in_printing_list[index]["started"] = util.get_current_time()
            pr.print_product(sprinter, assets_in_printing_list[index]["name"])
            time.sleep(5)
            # printer_status_list.append({"name": sprinter["name"], "product": assets_in_printing_list[index]["name"]})
            remove(sprinter, printers)
            print("printer is selected", sprinter)


class PrinterObserver(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args

        self.kwargs = kwargs
        return

    def run(self):
        # estimated printing duration is not involved in the system.
        global assets_in_printing_list

        while observer_running:
            print("observer is running")

            print("current asset list:", assets_in_printing_list)
            if len(assets_in_printing_list) > 0:
                printers = docker_manager.get_containers_details("octoprint")

                non_occupied_printers = []

                for printer in printers:
                    if pr.is_printer_free(printer):
                        non_occupied_printers.append(printer)

                if len(non_occupied_printers) > 0:
                    # filter the completed works
                    for printer in non_occupied_printers:
                        for item in assets_in_printing_list:
                            if item["assignedPrinterName"] == printer["name"] and item["status"] == "printing" and \
                                    check_printer_initiation_duration(item["started"]):
                                assets_in_printing_list.remove(item)
                                # remove item from the printer
                                #delete_product(printer, item) #

                    assign_printer(non_occupied_printers)

                else:
                    print("All printers are occupied...")

            else:
                print("Asset list is empty!")

            time.sleep(20)
        logging.info("Printer observer is stopping...")
        return


def start_observer():

    PrinterObserver(args=(), kwargs={'test': 'data'}).start()
    logging.info("Printer observer is started..")


def stop_observer():
    global observer_running
    observer_running = False
    logging.info("Printer observer is stopped ..")
