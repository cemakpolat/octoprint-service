"""
@author: Cem Akpolat
@created by cemakpolat at 2021-12-29
"""

import scheduler, docker_manager, util
from restapi import mainapi
logger = util.get_logger()

if __name__ == '__main__':
    logger.info("Printer Backend Service is starting...")
    docker_manager.start_printers(1)
    scheduler.start_observer()
    mainapi.run()
