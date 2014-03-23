import NNRequestHandler.Base
import NNRequestHandler.User



NN_REQUEST_CMD_USER_LOGIN = 1


class DispatchCenter(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DispatchCenter, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.cache = {}

        map = self.commandMap()
        for item in map:
            for command in item:
                self.installHandler(command, item[command])

    def commandMap(self):
        return [
            {NN_REQUEST_CMD_USER_LOGIN : NNRequestHandler.User.LoginHandler}
        ]

    def installHandler(self, command, HandlerClass):
        if command <= 0:
            raise "Command number less than 0"
        
        if not issubclass(HandlerClass, NNRequestHandler.Base.RequestHandler):
            raise "Request handler class must be subclass of RequestHandler"

        self.cache[command] = HandlerClass

    def dispatch(self, uin, command, body):
        if command not in self.cache:
            raise "Unknow Command %d" % (command)

        handlerClass = self.cache[command]
        handler = handlerClass(uin, body)
        handler.checkParams()
        handler.proccess()
        handler.dump()
        return (handler.retCode, handler.rspBody)
    
