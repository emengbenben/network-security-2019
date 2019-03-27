##====================================================================
# Assignment: Lab 1 Milestone 1 - Handshake - PIMP Packet
# Team: GoldenNugget
# Date: 03-25-2019
#====================================================================
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT16, STRING, UINT8, UINT32, BUFFER, BOOLEAN
import hashlib

class PIMPPacket(PacketType):
    TYPE_SYN = "SYN"
    TYPE_ACK = "ACK"
    TYPE_FIN = "FIN"
    TYPE_DATA = "DATA"
    DEFINITION_IDENTIFIER = "PIMP.Packet"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
        ("seqNum", UINT32),
        ("ackNum", UINT32),
      	("ACK", BOOLEAN),
      	("RST", BOOLEAN),
      	("SYN", BOOLEAN),
      	("FIN", BOOLEAN),
      	("RTR", BOOLEAN),
      	("checkSum", BUFFER),
        ("data", BUFFER),
      	#("window",UINT16)
		]
    # Class for Checksum related calculations
    def Cal_checksum(self):
        self.Checksum = b"0"
        GNByte = self.__serialize__()
        hash_value = hashlib.sha256()
        hash_value.update(GNByte)
        return hash_value.digest()
    
    def verfiyChecksum(self):
      oldChksum = self.Checksum
      newChksum = self.Cal_checksum()
      self.Checksum = newChksum
      if oldChksum == newChksum:
        return True
      else:
        return False
         
    # Packet definitions
    
    @classmethod
    def SynPacket(cls, seq):
        pkt = cls()
        pkt.Type = cls.TYPE_SYN
        pkt.SequenceNumber = seq    #seq = x
        #pkt.Cal_checksum()
        return pkt

    @classmethod
    def SynAckPacket(cls, seq, ack):
        pkt = cls()
        pkt.Type = cls.TYPE_SYN + cls.TYPE_ACK
        pkt.SequenceNumber = seq    #seq = y
        pkt.Acknowledgement = ack    #ack = seq(received) + 1
        #pkt.Cal_checksum()
        return pkt

    @classmethod
    def AckPacket(cls, ack):
        pkt = cls()
        pkt.Type = cls.TYPE_ACK
        pkt.Acknowledgement = ack     #ack = y + 1
        #pkt.Cal_checksum()
        return pkt

    @classmethod
    def DataPacket(cls, seq, data):
        pkt = cls()
        pkt.Type = cls.TYPE_DATA
        pkt.SequenceNumber = seq
        pkt.Data = data
        #pkt.Cal_checksum()
        return pkt
    
