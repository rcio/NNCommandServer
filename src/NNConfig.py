from ConfigParser import ConfigParser

DEFAULT_CONFIG_FILE_PATH = "/etc/nn.cfg"

dbHost = None
dbUser = None
dbPass = None
dbName = None

logFile = None
connectionLogFile = None
commandLogFile = None


def init():
    loadConfig()

def loadConfig():
    cfg = ConfigParser()
    fp = open(CONFIG_FILE_PATH, 'r')
    cfg.readfp(fp)

    global dbHost
    global dbUser
    global dbPass
    global dbName

    dbHost = cfg.get('Database', 'host')
    dbUser = cfg.get('Database', 'user')
    dbPass = cfg.get('Database', 'password')
    dbName = cfg.get('Database', 'db')
 
    global logFile
    global connectionLogFile
    global commandLogFile


if __name__ == "__main__" :
    init()

    print dbHost
    print dbUser
    print dbPass
    print dbName

        
