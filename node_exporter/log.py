import logging
import os, sys
from logging import handlers

logger = logging.getLogger(os.path.splitext(
    os.path.split((os.path.abspath(__file__)))[1])[0])
logger.setLevel(logging.INFO)
logFormatter = logging.Formatter('%(asctime)s - %(message)s')
fileHandler = handlers.RotatingFileHandler(
    '{}{}'.format(os.path.splitext(os.path.abspath(__file__))[0], '.log'),
    maxBytes=1024 * 1024 * 10,  # 10MB
    backupCount=10,
)
fileHandler.setFormatter(logFormatter)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)



