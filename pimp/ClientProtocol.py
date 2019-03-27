#====================================================================
# Assignment: Lab 1 Milestone 1 - Handshake - Protocol
# Team: GoldenNugget
# Date: 03-26-2019
#====================================================================
from playground.network.common import StackingProtocol, StackingProtocolFactory, StackingTransport
from .gnpacket import PIMPPacket
from .gntransport import PIMPTransport
import logging

class PIMPClientProtocol(StackingProtocol):
  #state definitions
  State_definition = {
    0:"DEFAULT",
    100:"CLOSED",
    101:"LISTEN",
    102:"Server_SYN-RECEIVED" ,
    103:"SERVER_TRANSMISSION",
    
    301:"CLIENT_INITIAL_SYN",
    302:"Client_SYN_SENT",
    303:"CLIENT_TRANSMISSION",
    304:"CLIENT_FIN_WAIT",
  }
  DEFAULT = 0
  CLOSED = 100
  LISTEN = 101
  CLIENT_INITIAL_SYN = 301
  Client_SYN_SENT = 302
  CLIENT_TRANSMISSION = 303
  CLIENT_FIN_WAIT = 304
  CLIENT_CLOSED = 305
  
  def __init__(self):
    super().__init__()
    self.seqNum = int.from_bytes(os.urandom(4), byteorder='big')
    self.client_seqNo = None
    self.state = DEFAULT
    self.client_state = self.CLIENT_INITIAL_SYN
    self.receivedDataBuffer = {}

  def logging_initialize(self):
      self.logger = logging.getLogger('transport_log')
      self.logger.setLevel(logging.DEBUG)
      # create file handler which logs even debug messages
      fd = logging.FileHandler('transport.log')
      fd.setLevel(logging.DEBUG)		
      # create console handler with a higher log level
      ch = logging.StreamHandler()
      ch.setLevel(logging.ERROR)
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      fh.setFormatter(formatter)
      ch.setFormatter(formatter)
      self.logger.addHandler(fh)
      self.logger.addHandler(ch)
        
  def sendSyn(self,transport):
    synPacket = PIMPPacket.SynPacket(self.seqNum)
    #logging
    self.logger.info('Sending SYN packet with Seq Number' + str(self.seqNum))
    transport.write(synPacket.__serialize__())
  
  def sendAck(self, transport):
    AckPacket = PIMPPacket.AckPacket(self.client_seqNum)
    self.logger.info('Sending ACK packet with Ack Number' + str(self.client_seqNum))
    transport.write(AckPacket.__serialize__())
  
  #def sendFinAck(self, transport):
    #function not defined 
  def processDatapkt(self, pkt):
    if self.state == self.CLIENT_CLOSED:
          self.logging.info("Connection closed")
    else:
          if pkt.seqNum == self.client_seqNum:
              self.logging.info("")
              self.client_seqNum = pkt.seqNum + len(pkt.Data)
              self.sendAck(self.transport)
              self.higherProtocol().data_received(pkt.Data)
              while self.client_seqNum in self.receivedDataBuffer:
                  (nxtPkt, receive_time) = self.receiveDataBuffer.pop(self.partnerSeqNumber)
                  self.client_seqNum = nxtPkt.SequenceNumber + len(nxtPkt.Data)
                  self.sendAck(self.transport)
                  self.higherProtocol().data_received(pkt.Data)
          elif pkt.seqNum > self.client_seqNum:
              self.logging.info()
              self.receiveDataBuffer[pkt.seqNum] = (pkt.time.time())
          else:
              self.logging.info("")
              ackNum = pkt.seqNum + len(pkt.Data)
              self.sendAck(self.transport)	
  
  def processAckPkt(self, pkt):
    self.logging.info("")
    latestAckNumber = pkt.ackNum
    
	
  def connection_made(self, transport):
      self.transport = transport
      if self.state == self.CLIENT_INTIAL_SYN:
          self.sendSyn(self.transport)
          self.seqNum += 1
          self.state = self.CLIENT_SYN_SENT
    
    
  def data_received(self,data):
     self.deserializer.update(data)
     for pkt in self.deserializer.nextPackets():
            if isinstance(pkt, PIMPPacket):   #check if this packet is an instance of PIMPPacket
                if pkt.verfiyChecksum():
                    if ("SYN" in pkt.Type) and ("ACK" in pkt.Type) and (self.state == self.CLIENT_SYN_SENT):
                            # check ack num
                        if(pkt.ackNum == self.seqNum):
                          self.logging.info("SYN-ACK with sequence number" + str(pkt.seqNum) + ", ack number" + str(pkt.ackNum))
                          self.state = self.CLIENT_TRANSMISSION
                          self.client_seqNum = pkt.seqNum + 1
                          self.sendAck(self.transport)
                          higherTransport = PIMPTransport(self.transport, self)
                          
                        else:
                          self.logging.info()
                      
                    elif(pkt.Type == "ACK") and (self.state == self.CLIENT_TRANSMISSION):
                       self.processAckpkt(pkt)
                    
                    elif(pkt.Type == "DATA") and (self.state == self.CLIENT_TRANSMISSION):
                       self.processDatapkt(pkt)  
                    else:
                      self.logging.info("Client: Wrong packet: seq num " + pkt.seqNum + ", type" + pkt.Type)
                else:
                  self.logging.info("Error in packet, checksum mismatch"+ str(pkt.Checksum))
            else:
               self.logging.info("Wrong packet class type "+ str(type(pkt)))
  
  def connection_lost(self, error):
    self.higherProtocol().connection_lost(error)
    self.logging.info()
    self.transport = None