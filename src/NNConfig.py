from ConfigParser import ConfigParser

DEFAULT_CONFIG_FILE_PATH = "/etc/nn.cfg"

nnConfig = None

configMap = [
    ['listenAddr', 'Listen', 'address', '127.0.0.1'],
    ['listenPort', 'Listen', 'port', 8888],

    ['dbHost', 'Database', 'host',     None],
    ['dbUser', 'Database', 'user',     None],
    ['dbPass', 'Database', 'password', None],
    ['dbName', 'Database', 'db',       None],

    ['logFilePath',        'Log', 'log_file_path',            '/var/log/nn/nn.log'],
    ['connLogFilePath',    'Log', 'connection_log_file_path', '/var/log/nn/connection.log'],
    ['commandLogFilePath', 'Log', 'command_log_file_path',    '/var/log/nn/command.log']
]

class Config():
    def __init__(self, path = DEFAULT_CONFIG_FILE_PATH):
        self.cfg = ConfigParser()
        fp = open(path, 'r')
        self.cfg.readfp(fp)
        self.loadConfig()

    def loadConfig(self):
        for item in configMap:
            setattr(self, item[0], self.getConfig(item[1], item[2], item[3]))
        

    def getConfig(self, section, option, default = None):
        value = None
        try:
            value = self.cfg.get(section, option)
        except:
            value = None
        
        if value == None:
            value = default

        return value
 
def init(configFilePath = DEFAULT_CONFIG_FILE_PATH):
    global nnConfig
    nnConfig = Config(configFilePath)


if __name__ == "__main__" :
    config = Config()
    print config.logFilePath
    print config.commandLogFilePath
    print config.dbName

        
