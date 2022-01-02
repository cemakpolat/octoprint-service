import threading
import time
import strategy_set, printer_observer as pr, util, infrastructure_manager

logger = util.get_logger()

PRINTER_INTIATION_MAX_DURATION = 60
assets_in_printing_list = []
observer_running = True
printer_status_list = []


def add_to_asset_list(products):

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
        logger.warning("No product is added, since the product list empty!")
    return False


def remove(obj, printers):
    for item in printers:
        if item["name"] == obj["name"]:
            printers.remove(item)
            logger.info("{item} is removed".format(item=item["name"]))


def check_printer_initiation_duration(starttime):
    """
     Wait 60 seconds for printing initiation, if it is more than this time, this means the printing is already started
    """
    difference = util.time_difference_in_sec(util.get_current_time(), starttime)
    if difference > PRINTER_INTIATION_MAX_DURATION:
        return True


def assign_printer(printers):
    for index in range(len(assets_in_printing_list)):
        if len(printers) > 0 and assets_in_printing_list[index]["status"] == "waiting":
            sprinter = strategy_set.select_randomly(printers)
            assets_in_printing_list[index]["assignedPrinterName"] = sprinter["name"]
            assets_in_printing_list[index]["status"] = "printing"
            assets_in_printing_list[index]["started"] = util.get_current_time()
            pr.print_product(sprinter, assets_in_printing_list[index]["name"])
            time.sleep(5)
            # printer_status_list.append({"name": sprinter["name"], "product": assets_in_printing_list[index]["name"]})
            remove(sprinter, printers)
            logger.debug("printer is selected", sprinter)


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
            logger.info("observer is running, current printing list")
            logger.info(assets_in_printing_list)
            if len(assets_in_printing_list) > 0:
                printers = infrastructure_manager.get_containers_details("octoprint")

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
                    logger.info("All printers are occupied...")

            else:
                logger.info("Asset list is empty!")

            time.sleep(20)
        logger.info("Printer observer is stopping...")
        return


def start_observer():

    PrinterObserver(args=(), kwargs={'': ''}).start()
    logger.info("Printer observer is started..")


def stop_observer():
    global observer_running
    observer_running = False
    logger.info("Printer observer is stopped ..")
