import socket
import select
import errno
import NNLogger
import NNError
import traceback

class TCPConnectionHandle(object):
    def __init__(self, socket, addr, port):
        self.socket = socket
        self.peerAddr = addr
        self.peerPort = port
        self.handleAccept()

    def handleAccept(self):
        NNLogger.logConnection("[ACCEPT] %s:%d" % (self.peerAddr, self.peerPort))

    def handleRead(self, data):
        pass

    def handleWrite(self):
        pass

    def handleClose(self, errCode):
        NNLogger.logConnection("[CLOSE] %s:%d %d" % (self.peerAddr, self.peerPort, errCode))



class TCPServer():
    def __init__(self, address, port, connClass):
        self.connMap = {}
        self.connClass = connClass

        self.addr = address
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((address, port))
        self.serverSocket.listen(1024)
        self.serverSocket.setblocking(0)

    def loop(self):
        rlist = [self.serverSocket]
        wlist = [self.serverSocket]

        while True:
            readFD, writeFD, exceptFD = select.select(rlist, wlist, []);
            for fd in readFD:
                if fd == self.serverSocket:
                    sock, (addr, port) = self.serverSocket.accept()
                    sock.setblocking(0)

                    try:
                        self.connMap[sock] = (self.connClass(sock, addr, port), sock, addr, port)
                        rlist.append(sock)
                    except Exception as e:
                        NNLogger.logConnection("[ERROR] Create instance of connection class [%s] error:%s" % (connClass, e))
                        sock.close()
                else:
                    ret = self.readDataFromFD(fd)
                    if ret <= 0:
                        fd.close()
                        self.connMap[fd][0].handleClose(ret)
                        rlist.remove(fd)
                        del self.connMap[fd]

    def readDataFromFD(self, fd):
        length = 0

        while True:
            try:
                data = fd.recv(8192)
                if len(data) == 0:
                    # Disconnect
                    return 0

                if fd in self.connMap:
                    try:
                        self.connMap[fd][0].handleRead(data)
                    except Exception as e:
                        NNLogger.logConnection("[ERROR] Handle read data from client (%s:%d) error:%s | %s" % (self.connMap[fd][2], self.connMap[fd][3], e, traceback.format_exc()))
                        return NNError.TCP_DATA_HANDLE_ERROR

                    length += len(data)
                else:
                    # Internal error
                    NNLogger.logConnection("[ERROR] Read FD not in cache")
                    return NNError.TCP_DATA_HANDLE_ERROR
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK:
                    # Read done
                    return length
                else:
                    # Other read error
                    return NNError.TCP_SOCK_READ_ERROR

if __name__ == '__main__':
    server = TCPServer('127.0.0.1', 8888, TCPConnectionHandle)
    server.loop()
