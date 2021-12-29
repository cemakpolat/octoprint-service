"""
@author: Cem Akpolat
@created by cemakpolat at 2021-11-13
"""
import requests, logging


def get_status_of_printer(printer):
    """
    This function retrieves the data from the given ip and port number. IP is currently not used.
    :param printer:
    :return:
    """
    port = {"port": printer["port"]}
    r = requests.get('http://localhost:8080/printer/status', params=port)
    return r.json()


def delete_product(printer, product):
    port = {"port": printer["port"], "product": product}
    r = requests.get('http://localhost:8080/product/delete', params=port)
    return r.json()


def print_product(printer, product):
    port = {"port": printer["port"], "product": product}
    r = requests.get('http://localhost:8080/printer/print', params=port)
    return r.json()


def is_printer_free(printer):
    response = get_status_of_printer(printer)
    print(response)
    if response["content"] == "OPERATIONAL" or response["content"] == "READY" or response["content"] == "CONNECTED":

        return True
    else:
        logging.debug("Printer cannot be selected since it is in the mode " + response["content"])

    return False
