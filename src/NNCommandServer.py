import NNTCPServer
import NNProtocol
import BBLogger

class NNCommandServer(TCPServer):
    def handle_stream(self, stream, address):
        BBLogger.info("New connection accept from %s", address)
        connection = NNConnection(stream)
        connection.readData()

class NNConnection(NNTCPServer.TCPConnectionHandle):
    def __init__(self, stream):
        self.buffer = ''
        self.requestPDU = None
    
    def handleRead(self, data):
        leftData = data

        while len(leftData):
            if not self.requestPDU:
                self.requestPDU = NNProtocol.NNRequestPDU()
                
            leftData = self.requestPDU.handleData(leftData)
            if self.requestPDU.allReceived:
                self.handleRequestPDU()
                self.requestPDU = None
            else:
                break
        

    def handleRequestPDU(self):
        print self.handleRequestPDU

if __name__ == '__main__':
    BBLogger.initLogger()

    server = NNTCPServer.TCPServer('127.0.0.1', 8888)
    server.loop()
