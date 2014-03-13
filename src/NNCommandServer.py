import NNConfig
import NNLogger
import NNTCPServer
import NNProtocol


class NNConnection(NNTCPServer.TCPConnectionHandle):
    def handleAccept(self):
        super(NNConnection, self).handleAccept()
        self.request = None


    def handleRead(self, data):
        leftData = data

        while leftData and len(leftData):
            if not self.request:
                self.request = NNProtocol.NNRequestPDU()
                
            leftData = self.request.handleData(leftData)
            if self.request.allReceived:
                self.handleRequestPDU()
                self.request = None
            else:
                break


    def handleRequestPDU(self):
        NNLogger.logCommand("Header: [%s] ---- Body: [%s]" % (self.request.header, self.request.bodyData))



if __name__ == '__main__':
    NNConfig.init()
    NNLogger.init()

    addr = NNConfig.nnConfig.listenAddr
    port = NNConfig.nnConfig.listenPort

    server = NNTCPServer.TCPServer(addr, port, NNConnection)
    server.loop()
