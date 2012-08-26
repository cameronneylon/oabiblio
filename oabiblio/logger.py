import logging
import logging.handlers
from logging import DEBUG

LOGFILE = "oabiblio.log"
LOGLEVEL = DEBUG
LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def log(name='oabiblio', logfile=LOGFILE, loglevel=LOGLEVEL, logformat=LOGFORMAT):
    log = logging.getLogger(name)
    log.setLevel(loglevel)

    if logfile:
        handler = logging.handlers.RotatingFileHandler(logfile, encoding="UTF-8")
    else:
        # log to stderr
        handler = logging.StreamHandler()

    formatter = logging.Formatter(logformat)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log
