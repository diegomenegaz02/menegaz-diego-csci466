import socket
import pickle
import sys
import time


class Packet():

    def __init__(self, sequence_number,checksum,ack_or_nak,length, message):
        self.sequence_number = sequence_number
        self.message = message
        self.checksum = checksum
        self.ack_or_nak = ack_or_nak
        self.length = length

    def set_checksum(self, sum):
        self.checksum  = sum
    def set_ack_or_nak(self, num):
        self.ack_or_nak = num
    def set_message(self, new_message):
        self.message = new_message
    def set_length(self,length):
        self.length = length
    def get_message(self):
        return self.message
    def get_length(self):
        return self.length
    def get_ack_or_nak(self):
        return self.ack_or_nak
    def get_checksum(self):
        return self.checksum
    def get_sequence(self):
        return self.sequence_number
def split_string(input_string, n):
    result = []
    for i in range(0, len(input_string), n):
        result.append(input_string[i:i + n])
    return result
def main():

    length =4
    messageCopy = "Hey what's up man"
    packet_list = []
    messagesplit = split_string(messageCopy,length)
    packetlen = len(messageCopy)
    if(messageCopy%length !=0):
        packetlen + length; #allows for another packet to be made to cover extra
    for i in range(packetlen/length):
        ob = Packet(i+1,"")
        packet_list.append(ob)
    for j in range(len(packet_list)):
        packet_list[i].set_message(messagesplit[i])
        packet_list[i].set_length(length)
        packet_list[i].set_checksum(True)
        packet_list[i].set_ack_or_nak(2);
    port = 6000
    host = socket.gethostname()
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket.connect( (host,port) )
    connection, addr = clientSocket.accept()
    while True:
        for each_packet in packet_list:
            data = pickle.dumps(each_packet)
            clientSocket.send(data)
            time.sleep(1)
            sData = connection.recv(1024)
            ack = pickle.loads(sData)
            if ack.get_ack_or_nak == 0:
                data = pickle.dumps(each_packet)
                clientSocket.send(data) #sending again if nak
                time.sleep(1)



#Okay PacketList set up to be sent.

