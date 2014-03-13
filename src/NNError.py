
TCP_DATA_HANDLE_ERROR = -101
TCP_SOCK_READ_ERROR  = -102

class error(Exception):
    def __init__(self, code):
        self.code = code
    
    def __str__(self):
        self.desc = self.errorDesc(code)
        return repr(self.desc)

    def errorDesc(self, code):
        pass
