import Base

class LoginHandler(Base.RequestHandler):
    def dump(self):
        self.rspBody = {'uin' : 1234}
