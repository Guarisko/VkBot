import logging;
import logging.handlers as handlers;

logger = logging.getLogger('vistaExchange');
logger.setLevel(logging.INFO);

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s');

logHandler = handlers.TimedRotatingFileHandler('logs//info.log', when='D', interval=1, backupCount=0);
logHandler.setLevel(logging.INFO);
logHandler.setFormatter(formatter);

errorLogHandler = handlers.TimedRotatingFileHandler('logs//error.log', when='D', interval=1, backupCount=0);
errorLogHandler.setLevel(logging.ERROR);
errorLogHandler.setFormatter(formatter);

logger.addHandler(logHandler);
logger.addHandler(errorLogHandler);

def getLogger():
    return logger;