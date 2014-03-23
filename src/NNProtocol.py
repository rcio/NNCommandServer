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
            if self.handleHeader() == False:
                return

        leftData = self.handleBody()
        return leftData


    def handleHeader(self):
        if len(self.buffer) >= NNReqHeader.size:
            self.header = NNReqHeader()
            self.header.handleData(self.buffer[:NNReqHeader.size])
            self.buffer = self.buffer[NNReqHeader.size:]
            return True
        else:
            return False;


    def handleBody(self):
        if len(self.buffer) >= self.header.bodyLen:
            self.bodyData = self.buffer[:self.header.bodyLen]
            self.body = json.loads(self.bodyData)
            self.allReceived = True;
            return self.buffer[self.header.bodyLen:]
        else:
            return

# Magic
# Seq
# Ret
# BodyLen
# Flag
# R1
# R2  
class NNRespHeader():
    def __init__(self, seq, ret, bodyLen):
        self.magic = magic
        self.seq = seq
        self.ret = ret
        self.bodyLen = bodyLen
        self.reserv1 = 0
        self.reserv2 = 0

        self.struct = struct.Struct('7I')

    def __str__(self):
        return '\nmagic : {self.magic}\nseq : {self.seq}\ncmd : {self.cmd}\nret : {self.ret}\nbodyLength : {self.bodyLen}\n'.format(self=self)
        
    def data(self, compress = False):
        self.flag = bool(compress) & compressFlag
        return self.struct.pack(self.magic,
                                self.seq,
                                self.ret,
                                self.bodyLen,
                                self.flag,
                                self.reserv1,
                                self.reserv2)

class NNResponsePDU():
    def __init__(self, seq, ret, body):
        self.bodyData = ''
        if len(body):
            self.bodyData = json.dumps(body)

        self.header = NNRespHeader(seq, ret, len(self.bodyData))

        self.body = body
        
    def data(self):
        resData = self.header.data()
        return resData + self.bodyData
