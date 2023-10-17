import socket
import pickle
import sys
import time

class Packet():
    def __init__(self, sequence_number, checksum, ack_or_nak, length, message):
        self.sequence_number = sequence_number
        self.message = message
        self.checksum = checksum
        self.ack_or_nak = ack_or_nak
        self.length = length


    def set_checksum(self, sum):
        self.checksum = sum


    def set_ack_or_nak(self, num):
     self.ack_or_nak = num


    def set_message(self, new_message):
        self.message = new_message


    def set_length(self, length):
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

def send_ACK(SN,checksum):
    if(checksum == True):
        ACK = Packet(SN,True,1,0,"")
        data = pickle.dumps(ACK)
    elif(checksum == False):
        NACK = Packet(SN,True,0,0,"")
        data = pickle.dumps(NACK)
    return data;
def main():
    recieved_packets = []
    port = 6000
    host = socket.gethostname()
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind( (host,port))
    serverSocket.listen(1)
    connection,addr= serverSocket.accept()
#idea recieve packet - send ACK - get another so each loop
    while True:
        data = connection.recv(1024)
        ob = pickle.loads(data)
        ack = send_ACK(ob.get_sequence(),ob.get_checksum)
        recieved_packets.append(ob)
        serverSocket.send(ack)
        time.sleep(1)
