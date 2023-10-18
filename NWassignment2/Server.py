import socket
import pickle
import sys
import time
import csv
import re


# Function to replace words in a string

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



def split_string(input_string, n):
    result = []
    for i in range(0, len(input_string), n):
        result.append(input_string[i:i + n])
    return result
def read_word_replacements(csv_file):
    word_replacements = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                word_replacements[row[0]] = row[1]
    return word_replacements
#This csv replacement ironically was a leet code problem :D So citing #1 Solution that I had already used.
def replace_words_with_csv(csv_file, input_string):
    word_replacements = read_word_replacements(csv_file)
    words = re.findall(r'\b\w+\b', input_string)  # Extract words from the input string
    result_string = []

    for word in words:
        if word in word_replacements:
            result_string.append(word_replacements[word])
        else:
            result_string.append(word)

    # Reconstruct the string while preserving punctuation
    result_string = re.sub(r'\b\w+\b', lambda m: result_string.pop(0), input_string)

    return result_string
def corruption(percent,array):
    if 0 <= percent <= 1:
        array_length = len(array)
        array_index = int(percent * (array_length-2))
        if array_index < array_length -1:
            array[array_index].set_checksum(False)

def main():
    length = int(sys.argv[2])
    packet_corruption = float(sys.argv[3])
    recieved_packets = []
    packet_list = []

    port = int(sys.argv[1])
    host = socket.gethostname()
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind( (host,port))
    serverSocket.listen(1)
    print("It is listening for connection")

    connection,addr= serverSocket.accept()

#idea recieve packet - send ACK - get another so each loop
    while True:
        data = connection.recv(1024)
        ob = pickle.loads(data)
        length = ob.get_length()
        if ob.get_checksum() == False:
            NACK = Packet(ob.get_sequence(), True, 0, 0, "NACK")
            sData = pickle.dumps(NACK)
            connection.send(sData)
            time.sleep(1)
        else:
            ACK = Packet(ob.get_sequence(), True, 1, 0, "ACK")
            recieved_packets.append(ob)
            sData = pickle.dumps(ACK)
            connection.send(sData)
            time.sleep(1)
        if "." in ob.get_message():
            break


#First Connection Above
#contacinate a string via the packets
    decrypted_message = ""
    for p in recieved_packets:
        decrypted_message = decrypted_message + p.get_message()
#String Reconstructed

    pirated_message = replace_words_with_csv("pirate.csv",decrypted_message)
    packetlen = len(pirated_message)
    print(pirated_message)
    messagesplit = split_string(pirated_message,length)
    if (packetlen % length != 0):
        packetlen = packetlen + length  # allows for another packet to be made to cover extra
    packetlen = packetlen / length
    packetlen = int(packetlen)
    for i in range(packetlen):
        ob = Packet(i + 1, True, 2, length, "")
        packet_list.append(ob)
    for j in range(len(packet_list)):
        packet_list[j].set_message(messagesplit[j])


    corruption(packet_corruption,packet_list)
    for each_packet in packet_list:
        data = pickle.dumps(each_packet)
        connection.send(data)
        time.sleep(1)
        Sdata = connection.recv(1024)
        ob = pickle.loads(Sdata)
        ACKm = ob.get_ack_or_nak()
        print(ob.get_message())
        if(ACKm == 0):
            each_packet.set_checksum(True)
            data = pickle.dumps(each_packet)
            connection.send(data)
            time.sleep(1)

        #print("Sending", each_packet.get_message())
        #print(ACKm)
#Waiting for Server to Grab Final repeated Message
if __name__ == '__main__':
    main()

