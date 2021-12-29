"""
@author: Cem Akpolat
@created by cemakpolat at 2021-12-28
"""


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
        self.climateEffect = "0"  # due to the consumed energy!
        self.device = "x-marke"


class ProductModel:
    def __init__(self):
        self.name = "Product Model Name"
        self.creator = "Beagle Bone"
        self.complexity = "100"  # 0-100


class Printer:
    def __init__(self):
        self.name = "Printer Name"
        self.features = ""


class User:
    def __init__(self, user_id):

        self.user_id = user_id
        self.eco = 33
        self.cost = 33
        self.time = 34

    def update_preferences(self, params):
        self.eco = params['eco']
        self.cost = params['cost']
        self.time = params['time']