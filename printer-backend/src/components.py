"""
@author: Cem Akpolat
@created by cemakpolat at 2021-12-28
"""
import json


class Process:
    def __init__(self):
        self.energy_consumption = 10
        self.climate_effect = 3/10
        self.cost = 0


class DeliveryType:

    def __init__(self):
        self.cost = "0"
        self.energy_consumption = "10"
        self.climate_effect = "3/10"
        self.owner = "company"
        self.duration = "10"
        self.type = "drone"


class Printer:
    """
    The purpose of this class is to select the best option that can be used
    In the future, other parameters should be also involved here to make the decision harder
    The printer owners would have different devices, quality, delivery time as well as cost
    The decision will be based on those parameters.
    """

    def __init__(self, owner, quality, cost, energyComsumption):
        self.owner = "name"
        self.quality = "resolution"
        self.cost = "0-100"
        self.possibleEnergyConsumption = "100"
        self.climateEffect = "0"  # due to the consumed energy!
        self.device = "x-marke"


class Product:
    def __init__(self, name, creator, complexity):
        self.name = "Product Model Name"
        self.creator = "Beagle Bone"
        self.complexity = "100"  # 0-100


class User:
    def __init__(self, user_id, eco=33, cost=33, time=34):
        self.user_id = user_id
        self.eco = eco
        self.cost = cost
        self.time = time

    def update_preferences(self, params):
        self.eco = params['eco']
        self.cost = params['cost']
        self.time = params['time']


def import_json_files():
    """
    Convert json model to the app. class object
    model = '{"name":"cem","username":"akpolat"}'
    j = json.loads(model)
    u = User(**j)
    :return:
    """
    pass

