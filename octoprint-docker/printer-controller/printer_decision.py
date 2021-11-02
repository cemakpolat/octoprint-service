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


def selectPrinter():
    printers = docker_interface.get_containers_details()

    for printer in printers:
        print(printer)
        # call rest of the java app
        # see the printer is not printing
        # select randomly the printer
    """
    1. get all port numbers from docker-interface
    2. call the java api for each port to see whether the printer is running or not
    3. create a list of available printers
    4. choose randomly one of the printers
    5. future task: based on the printer features, take different decisions.
    """
    # select one of it

    return "printer-id and port"

