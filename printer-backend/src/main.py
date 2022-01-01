"""
@author: Cem Akpolat
@created by cemakpolat at 2021-12-29
"""

import printer_decision, docker_manager, util
from restapi import main_api
logger = util.get_logger()

if __name__ == '__main__':
    logger.info("Printer Backend Service is starting...")
    docker_manager.start_printers(1)
    printer_decision.start_observer()
    main_api.run()
