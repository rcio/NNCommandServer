import NNError


class RequestHandler(object):
    def __init__(self, uin, body):
        self.uin = uin
        self.reqBody = body
        self.rspBody = ''
        self.retCode = NNError.NN_ERR_NO_ERROR
        self.retMsg = ''

    def checkParams(self):
        pass

    def proccess(self):
        pass

    def dump(self):
        pass

