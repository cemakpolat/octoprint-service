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

    def __init__(self, owner, quality, cost, deliveryTime, energyComsumption):
        self.owner = "name"
        self.quality = "resolution"
        self.cost = "0-100"
        self.deliveryTime = "3"
        self.possibleEnergyConsumption = "100"
        self.climateEffect = "0"  # due to the consumed energy!
        self.device = "x-marke"


class ProductModel:
    def __init__(self, name, creator, complexity):
        self.name = "Product Model Name"
        self.creator = "Beagle Bone"
        self.complexity = "100"  # 0-100


class Printer:
    def __init__(self):
        self.name = "Printer Name"
        self.features = ""


class User(object):
    def __init__(self, user_id, eco=33, cost=33, time=34):

        self.user_id = user_id
        self.eco = eco
        self.cost = cost
        self.time = time

    def update_preferences(self, params):
        self.eco = params['eco']
        self.cost = params['cost']
        self.time = params['time']


class User:
    def __init__(self, name, username):
        self.name = name
        self.username = username

import json
model = '{"name":"cem","username":"akpolat"}'
j = json.loads(model)
print(j)
u = User(**j)
