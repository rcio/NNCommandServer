import socket
import select
import errno

class TCPConnectionHandle():
    def __init__(self, socket, addr, port):
        self.socket = socket
        self.peerAddr = addr
        self.peerPort = port
        self.handleAccept()

    def handleAccept(self):
        print ("New connection from %s coming.." % self.peerAddr)

    def handleRead(self, data):
        print ("Recv data: %s" % data)

    def handleWrite(self):
        pass

    def handleClose(self, errCode):
        pass



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
                    rlist.append(sock)

                    self.connMap[sock] = self.connClass(sock, addr, port)
                else:
                    if self.readDataFromFD(fd) <= 0:
                        fd.close()
                        self.connMap[fd].handleClose()
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
                    self.connMap[fd].handleRead(data)
                    length += len(data)
                else:
                    # Internal error
                    return -1
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK:
                    # Read done
                    return length
                else:
                    # Other read error
                    return e.errno

if __name__ == '__main__':
    server = TCPServer('127.0.0.1', 8888, TCPConnectionHandle)
    server.loop()
