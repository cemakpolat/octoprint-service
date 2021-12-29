"""
@author: Cem Akpolat
@created by cemakpolat at 2021-12-29
"""
import json, logging
from flask import jsonify, Blueprint, request
from src import printer_decision

printingapi = Blueprint('printingapi', __name__)

logger = logging.getLogger()


@printingapi.route('/printers/select', methods=["GET", "POST"])
def assign_printer():
    product_list = request.form.getlist('products[]')
    # print("Assets to be printed:", product_list)

    if product_list and printer_decision.add_to_asset_list(product_list):
        res = "The {products} are added to the list".format(products=str(product_list))
    else:
        res = "The product list is empty!"
        logger.warning("container name is not given as a parameter")

    return json.dumps({"result": res})


@printingapi.route('/printers/assets/status', methods=["GET", "POST"])
def get_ordered_asset_statuses():
    return jsonify(printer_decision.assets_in_printing_list);


@printingapi.route('/printers/assets', methods=["GET", "POST"])
def get_assets_in_printing_process():
    return json.dumps({"result": printer_decision.assets_in_printing_list})
