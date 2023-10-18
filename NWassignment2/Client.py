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
def corruption(percent,array):
    if 0 <= percent <= 1:
        array_length = len(array)
        array_index = int(percent * (array_length-2))
        if array_index < array_length -1:
            array[array_index].set_checksum(False)
def main():
    packet_corruption = float(sys.argv[3]) #will be ARGS
    length = int(sys.argv[2])
    messageCopy = "you are an idiot."
    packetlen = len(messageCopy)
    packet_list = []
    messagesplit = split_string(messageCopy,length)

    if(packetlen%length !=0):
        packetlen = packetlen + length; #allows for another packet to be made to cover extra
    packetlen = packetlen/length
    packetlen = int(packetlen)
    for i in range(packetlen):
        ob = Packet(i+1,True,2,length,"")
        packet_list.append(ob)
    for j in range(len(packet_list)):
        packet_list[j].set_message(messagesplit[j])
    corruption(packet_corruption,packet_list)
    #Corruption Here
    port = int(sys.argv[1])
    host = socket.gethostname()
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket.connect( (host,port) )

    for each_packet in packet_list:
        data = pickle.dumps(each_packet)
        clientSocket.send(data)
        time.sleep(1)
        #If not corrupted
        Sdata = clientSocket.recv(1024)
        ob = pickle.loads(Sdata)
        ACKm = ob.get_ack_or_nak()
        print(ob.get_message())

        if(ACKm == 0):#sending packet uncorrupted
            each_packet.set_checksum(True)
            data = pickle.dumps(each_packet)
            clientSocket.send(data)
            time.sleep(1)

        #print("Sending", each_packet.get_message())
        #print(ACKm)

#Server Now is going to Send Message Back Meaning we need to Send Acks.

    recieved_packets = []
    while True:
        data = clientSocket.recv(1024)
        ob = pickle.loads(data)
        length = ob.get_length()
        if ob.get_checksum() == False:
            NACK = Packet(ob.get_sequence(), True, 0, 0, "NACK")
            sData = pickle.dumps(NACK)
            clientSocket.send(sData)
            time.sleep(1)
        else:
            ACK = Packet(ob.get_sequence(), True, 1, 0, "ACK")
            recieved_packets.append(ob)
            sData = pickle.dumps(ACK)
            clientSocket.send(sData)
            time.sleep(1)
        if "." in ob.get_message():
            break
    decrypted_message = ""
    for p in recieved_packets:
        decrypted_message = decrypted_message + p.get_message()
    print(decrypted_message)




if __name__ == '__main__':
    main()


#TODO: Create the random chance for NAK,
#TODO: Got acks working/got message->server->pirated->Client