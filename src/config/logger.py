import logging

# Logging config
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')



def logInfo(message):
    logging.info(f'{message}')
def logDebug(message):
    logging.debug(f'{message}')
def logDebug(message):
    logging.warning(f'{message}')
def logDebug(message):
    logging.error(f'{message}')
def logDebug(message):
    logging.critical(f'{message}')