import struct

maxBodyLen = 2 * 1024 * 1024

magic = 0x12345678
compressFlag = 0x00000001

class NNReqHeader():
    size = 28
    
    def __init__(self):
        self.struct = struct.Struct('7I')


    def __str__(self):
        return '\nmagic : {self.magic}\nseq : {self.seq}\ncmd : {self.cmd}\nbodyLength : {self.bodyLen}\n'.format(self=self)

    def handleData(self, data):
        if len(data) != NNReqHeader.size:
            raise "Packet header size error"

        headerTuple = self.struct.unpack(self.data)
        self.magic = headerTuple[0]
        self.seq = headerTuple[1]
        self.cmd = headerTuple[2]
        self.bodyLen = headerTuple[3]
        self.flag = headerTuple[4]
        self.reserv1 = headerTuple[5]
        self.reserv2 = headerTuple[6]
        
        self.isCompressed = bool(self.flag & compressFlag)

    def check(self):
        if (self.magic != magic):
            raise "Packet header magic wrong"
        if (self.bodyLen > maxBodyLen):
            raise "Packet body too big"

class NNRequestPDU():
    def __init__(self):
        self.buffer = ''
        self.bodyData = ''
        self.allReceived = False
        self.reqHeader = None
        
    def handleData(self, data):
        if not self.allReceived:
            self.buffer.append(data)
        else:
            return;

        if not self.reqHeader:
            if len(self.buffer) >= NNReqHeader.size:
                self.reqHeader = NNReqHeader()
                self.reqHeader.handleData(self.buffer[:NNReqHeader.size])
                self.buffer = self.buffer[NNReqHeader.size:]
            else:
                return;
        else:
            if len(self.buffer) >= self.reqHeader.bodyLen:
                self.bodyData = self.buffer[:self.reqHeader.bodyLen]
                self.allReceived = True;
                return self.buffer[self.reqHeader.bodyLen:]
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
