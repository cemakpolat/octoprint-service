"""
@author: Cem Akpolat
@created by cemakpolat at 2021-12-29
"""

import printing_scheduler, infrastructure_manager, util
from restapi import mainapi
logger = util.get_logger()

if __name__ == '__main__':
    logger.info("Printer Backend Service is starting...")
    # infrastructure_manager.start_printers(1)
    printing_scheduler.start_observer()
    mainapi.run()
