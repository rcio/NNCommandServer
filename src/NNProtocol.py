import struct
import json

maxBodyLen = 2 * 1024 * 1024

magic = 0x12345678
compressFlag = 0x00000001

class NNReqHeader():
    size = 32
    
    def __init__(self):
        self.struct = struct.Struct('8I')


    def __str__(self):
        return 'magic : {self.magic} | uin : {self.uin} | seq : {self.seq} | cmd : {self.cmd} | bodyLength : {self.bodyLen}'.format(self=self)

    def handleData(self, data):
        if len(data) != NNReqHeader.size:
            raise "Packet header size error"

        headerTuple = self.struct.unpack(data)
        self.magic = headerTuple[0]
        self.uin = headerTuple[1]
        self.seq = headerTuple[2]
        self.cmd = headerTuple[3]
        self.bodyLen = headerTuple[4]
        self.flag = headerTuple[5]
        self.reserv1 = headerTuple[6]
        self.reserv2 = headerTuple[7]
        
        self.isCompressed = bool(self.flag & compressFlag)

    def check(self):
        if (self.magic != magic):
            raise "Packet header magic wrong"
        if (self.bodyLen > maxBodyLen):
            raise "Packet body too big"

class NNRequestPDU():
    def __init__(self):
        self.buffer = ''
        self.header = None
        self.bodyData = None
        self.allReceived = False

        
    def handleData(self, data):
        if not self.allReceived:
            self.buffer += data

        if not self.header:
            self.handleHeader()

        leftData = self.handleBody()
        return leftData


    def handleHeader(self):
        if len(self.buffer) >= NNReqHeader.size:
            self.header = NNReqHeader()
            self.header.handleData(self.buffer[:NNReqHeader.size])
            self.buffer = self.buffer[NNReqHeader.size:]
        else:
            return;


    def handleBody(self):
        if len(self.buffer) >= self.header.bodyLen:
            self.bodyData = self.buffer[:self.header.bodyLen]
            self.body = json.loads(self.bodyData)
            self.allReceived = True;
            return self.buffer[self.header.bodyLen:]
        else:
            return
        
class BPRespHeader():
    def __init__(self, aTuple):
        self.magic = aTuple[0]
        self.seq = aTuple[1]
        self.cmd = aTuple[2]
        self.ret = aTuple[3]
        self.bodyLen = aTuple[4]
        self.flag = aTuple[5]
        self.reserv1 = aTuple[6]
        self.reserv2 = aTuple[7]

    def __str__(self):
        return '\nmagic : {self.magic}\nseq : {self.seq}\ncmd : {self.cmd}\nret : {self.ret}\nbodyLength : {self.bodyLen}\n'.format(self=self)


class BPBody():
    def __init__(self, data):
        self.data = data


class BPRequest():
    def __init__(self, header, body):
        self.header = header
        self.body = body


class BPResponse():
    def __init__(self, header, body):
        self.header = header
        self.body = body
