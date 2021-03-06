"""
@author: Cem Akpolat
@created by cemakpolat at 2021-12-29
"""

from flask import jsonify, Blueprint, request
import printing_scheduler, util

printingapi = Blueprint('printingapi', __name__)

logger = util.get_logger()


@printingapi.route('/printers/select', methods=["GET", "POST"])
def assign_printer():
    product_list = request.form.getlist('products[]')

    if product_list and printing_scheduler.add_to_asset_list(product_list):
        res = "The {products} are added to the list".format(products=str(product_list))
        return jsonify({"message": res, "type": "success"})
    else:
        res = "The product list is empty!"
        logger.warning("container name is not given as a parameter")
        return jsonify({"message": res, "type": "error"})


@printingapi.route('/printers/assets/status', methods=["GET", "POST"])
def get_ordered_asset_statuses():
    return jsonify({"message": printing_scheduler.assets_in_printing_list, "type": "success"})


@printingapi.route('/printers/assets', methods=["GET", "POST"])
def get_assets_in_printing_process():
    return jsonify({"message": printing_scheduler.assets_in_printing_list, "type": "success"})
