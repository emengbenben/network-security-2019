#====================================================================
# Assignment: Lab 1 Milestone 1 - Handshake - Transport
# Team: GoldenNugget
# Date: 03-26-2019
# https://github.com/Tony96301/Network-Security/blob/master/programming%20realization/tcp_layer/ServerProtocol.py
#====================================================================

from playground.network.common import StackingTransport
from .PIMPPacket import PIMPPacket
import asyncio
import random

class PIMPTransport(StackingTransport):   #inherit the stackingtransport class
    CHUNK_SIZE = 1500    #each packet is

    def __init__(self, transport, protocol=None):
        super().__init__(transport)
        self.protocol = protocol   #the protocol instance are put in from client or server protocol

    def write(self, data):    #mimic the stackingtransport class
        if self.protocol:
            if not self.protocol.isClosing():

                i = 0
                index = 0
                sentData = None
                while (i < len(data)):   #the serialized http packet is split into several chunks
                    if (i + self.CHUNK_SIZE < len(data)):
                        sentData = data[i: i + self.CHUNK_SIZE]
                    else:
                        sentData = data[i:]
                    i += len(sentData)   #the length of sentData is always 38, why is it???
                    #whether to change the seqNum, depends on the PIMP's definition
                    pkt = PIMPPacket.DataPacket(self.protocol.seqNum, sentData)   #make a data packet with one chunk bytes
                    index += 1
                    ackNumber = self.protocol.seqNum + len(sentData)  #the next ack_num we should get for our last sent data packet

                    #we create a sentdata_cache to contain those data packets sent without receiving corresponding ack packets
                    if len(self.protocol.sentDataCache) <= self.protocol.WINDOW_SIZE:   #there is window space for packet to send immediately
                        print("PIMPTransport: Sending packet {!r}, sequence number: {!r}".format(index, pkt.SequenceNumber))
                        self.protocol.transport.write(pkt.__serialize__())
                        self.protocol.sentDataCache[ackNumber] = (pkt)  #Removed the Timestamp

                    else:
                        print("PIMPTransport: Buffering packet {!r}, sequence number: {!r}".format(index, pkt.SequenceNumber))
                        #if the window is fully used, then we need to put packets waiting to send into sending buffer
                        self.protocol.sendingDataBuffer.append((ackNumber, pkt))
                        # self.protocol.sendNextDataPacket()

                    self.protocol.seqNum += len(sentData)
                print("PIMPTransport: Batch transmission finished, number of packets sent: {!r}".format(index))
            else:
                print("PIMPTransport: protocol is closing, unable to write anymore.")

        else:
            print("PIMPTransport: Undefined protocol, writing anyway...")
            print("PIMPTransport: Write got {} bytes of data to pass to lower layer".format(len(data)))
            super().write(data)
        # self.protocol.sendNextDataPacket()

    def close(self):
        if not self.protocol.isClosing():
            print("Prepare to close...")
            self.protocol.prepareForFin()
        else:
            print("PIMPTransport: Protocol is already closing.")