import logging

# Config
LOG_FILE_PATH = '/var/log/bobo/bobo.log'
CONN_FILE_PATH = '/var/log/bobo/connection.log'
COMMAND_FILE_PATH = '/var/log/bobo/command.log'

nnLogger = None
connLogger = None
commandLogger = None

debug = None
info = None
warning = None
error = None

logConnection = None
logCommand = None

def init():
    global nnLogger
    global connLogger
    global commandLogger

    global debug
    global info
    global warning
    global error

    global logConnection
    global logCommand

    nnLogger = createLogger('NN', LOG_FILE_PATH, '%(levelname)-7s %(asctime)-10s  [%(filename)s:%(lineno)d]  %(message)s')
    connLogger = createLogger('Connection', CONN_FILE_PATH, '%(asctime)-10s %(message)s')
    commandLogger = createLogger('Command', COMMAND_FILE_PATH, '%(asctime)-10s %(message)s')

    debug = nnLogger.debug
    info = nnLogger.info
    warning = nnLogger.warning
    error = nnLogger.error

    logConnection = connLogger.info
    logCommand = commandLogger.info

def createLogger(name, filePath, formatStr):
    formatter = logging.Formatter(formatStr)
    logger = logging.getLogger(name)

    fileHandler = logging.FileHandler(filePath)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    
    if __debug__:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)
        
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    
    return logger

if __name__ == '__main__':
    initLogger()

    debug("sdfdf")
    debug("test")
    warning("test")
    info("test")
    error("test")
