#====================================================================
# Assignment: Lab 1 Milestone 1 - Handshake - Protocol
# Team: GoldenNugget
# Date: 03-26-2019
#====================================================================
from playground.network.common import StackingProtocol, StackingProtocolFactory, StackingTransport
from .gnpacket import PIMPPacket
from .gntransport import PIMPTransport
import logging
import os

class PIMPServerProtocol(StackingProtocol):
  #state definitions
  State_definition = {
    0:"DEFAULT",
    100:"CLOSED",
    101:"LISTEN",
    102:"SERVER_SYN-RECEIVED" ,
    103:"SERVER_TRANSMISSION",
    
    301:"CLIENT_INITIAL_SYN",
    302:"Client_SYN_SENT",
    303:"CLIENT_TRANSMISSION",
    304:"CLIENT_FIN_WAIT",
  }
  
  DEFAULT = 0
  CLOSED = 100
  LISTEN = 101
  SERVER_SYN_RECEIVED = 102
  SERVER_TRANSMISSION =103

  def __init__(self):
    super().__init__()
    self.seqNo = int.from_bytes(os.urandom(4), byteorder='big')
    self.client_seqNo = None
    self.state = self.DEFAULT
    self.sentDataCache = {}
    self.receivedDataBuffer = {}   #receive the packet which is out of order
    # create logger with 'spam_application'
    self.logger = logging.getLogger('transport_log')
    self.logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fd = logging.FileHandler('transport.log')
    fd.setLevel(logging.DEBUG)
	# create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fd.setFormatter(formatter)
    ch.setFormatter(formatter)
    self.logger.addHandler(fd)
    self.logger.addHandler(ch)
    
  def sendSyn(self,transport):
    synPacket = PIMPPacket.SynPacket(self.seqNo)
    #logging
    self.logger.info('Sending SYN packet with Seq Number' + str(self.seqNo))
    transport.write(synPacket.__serialize__())
    
  def sendSynAck(self, transport,SynAck_seqNo):
    synAckPacket = PIMPPacket.SynAckPacket(SynAck_seqNo, self.client_ackNo)
    #logging
    self.logger.info('Sending SYN_ACK packet with Seq Number ' + str(SynAck_seqNo) + ' Ack Number ' +  str(self.client_ackNo))
    transport.write(synAckPacket.__serialize__())
  
  def sendAck(self, transport):
    AckPacket = PIMPPacket.AckPacket(self.client_seqNo)
    self.logger.info('Sending ACK packet with Ack Number' + str(self.client_seqNo))
    transport.write(AckPacket.__serialize__())
    
  #def sendFin(self, transport):
    #function not defined 
  def connection_made(self, transport):
    self.transport = transport
  
  def processAckPkt(self,pkt):
        latestAckNumber = pkt.ackNum  #the ackNum of the last ack packet we get
        while latestAckNumber in list(self.sentDataCache):  #when there is an ackNum stacked in the sent_buffer
            print ("Received ACK for dataSeq: {!r}, removing".format(self.sentDataCache[latestAckNumber][0].seqNum))
            del self.sentDataCache[latestAckNumber]    #delete the data packet from the sent buffer
            break
            
  def processDataPkt(self, pkt):
    if self.state == self.CLOSED:
        self.logging.info("Connection closed")
    else:
      if pkt.seqNum == self.client_seqNo:  # the data with the seq_num is exactly what we want
        self.client_seqNo = pkt.seqNum + len(pkt.Data)  # update the ack_num for next packet, y + len(data) -> ack_num
        self.sendAck(self.transport)  #send the corresponding ack packet
        self.higherProtocol().data_received(pkt.Data)  # upload the data to higher level
        while self.client_seqNo in self.receivedDataBuffer:# transmit the packet with higher seq_num than expectation we get before to higher layer
              (nextPkt, receive_time) = self.receivedDataBuffer.pop(self.client_seqNo)
              self.client_seqNo = nextPkt.seqNum + len(nextPkt.Data) # update the ack_num for next packet, y + len(data) -> ack_num
              self.sendAck(self.transport)  # send the corresponding ack packet
              self.higherProtocol().data_received(nextPkt.Data)  # upload the data to higher level--http
      elif pkt.seqNum > self.client_seqNum:
          self.logging.info()
          self.receiveDataBuffer[pkt.seqNum] = (pkt.time.time())

      else:
          self.logging.info("")
          ackNum = pkt.seqNum + len(pkt.Data)
          self.sendAck(self.transport) 

  
  def data_received(self,data):
    self.deserializer.update(data)
    for pkt in self.deserializer.nextPackets():
          if isinstance(pkt, PIMPPacket):
              if pkt.verfiyChecksum():   #check whether there is error appeared in any one tcp packet
                  if  pkt.Type == "SYN" and self.state == self.LISTEN:
                    self.state = self.Server_SYN_RECEIVED
                    self.client_seqNo = pkt.seqNum + 1
                    SynAck_seqNo  = self.seqNo
                    self.sendSynAck(self.transport,SynAck_seqNo)
                    self.seqNo += 1
                  elif pkt.Type == "ACK" and self.state == self.Server_SYN_RECEIVED:
                    if pkt.ackNum == self.seqNo:
                      self.state = self.SERVER_TRANSMISSION
                      higherTransport = PIMPTransport(self.transport,self)
                      self.higherProtocol().connection_made(higherTransport)
                      
                    else:
                      print("Server: Wrong ACK packet: ACK number: {!r}, expected: {!r}".format(
                                    pkt.ackNum, self.seqNo))
                  elif (pkt.Type == "DATA") and (self.state == self.SERVER_TRANSMISSION):
                        self.processDataPkt(pkt)
									
                  elif (pkt.Type == "ACK") and (self.state == self.SERVER_TRANSMISSION):
                        self.processAckPkt(pkt)
                  else:
                    self.logging.info("Server: Wrong packet: seq num " + pkt.seqNum + ", type" + pkt.Type)
              else:
                  self.logging.info("Error in packet, checksum mismatch"+ str(pkt.Checksum))
          else:
               self.logging.info("Wrong packet class type "+ str(type(pkt)))        