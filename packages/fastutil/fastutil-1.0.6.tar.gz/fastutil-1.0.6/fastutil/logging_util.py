import logging
from logging.handlers import TimedRotatingFileHandler

LOGGING_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'


def set_rotating_logger(log_name, log_path):
    formatter = logging.Formatter(LOGGING_FORMAT)
    file_handler = TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=15)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
