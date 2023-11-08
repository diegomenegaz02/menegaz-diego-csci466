import requests
import csv
url1 = "https://www.cs.montana.edu/pearsall/classes/fall2023/466/programs/prefix_matching.csv"
url2 = "https://www.cs.montana.edu/pearsall/classes/fall2023/466/programs/packets.csv"
def occurence(input_string, char_to_delete):
    result = ''.join(char for char in input_string if char != char_to_delete)
    return result
addresses = []
def make_request(Url, determine):
    if determine == "SaveAddresses":
        response = requests.get(Url)
        if response.status_code == 200:
            longer_string = response.text
            packets1 = longer_string.split("\n")

            del packets1[0]
            return packets1

    if determine == 'FT':
        response = requests.get(Url)
        if response.status_code == 200:
            long_string = response.text
            addresses = list(csv.reader(long_string.splitlines()))
            del addresses[0]
            interace_dict = {}
        placeholder = ""
        for row in addresses:
            for i in range (0,len(row[0]), 8):
                bits = row[0][i:i+8]
                placeholder += bits + '.'
            placeholder = placeholder[:-1]
            key = row[1]
            value = placeholder
            interace_dict[key] = value
            placeholder = ""
        return interace_dict
    elif determine == 'Packet':
        packets = []
        response = requests.get(Url)
        if response.status_code == 200:
            longer_string = response.text
            packets1 = longer_string.split("\n")
            del packets1[0]
        for each in packets1:
            binary = ('.'.join([bin(int(x) + 256)[3:] for x in each.split('.')]))
            packets.append(binary)
        return packets

def comparingFWDtable(fwd,pl,addr):
    for j in range (0,len(pl)):
        for key in fwd:
            noStars = occurence(fwd.get(key),'*')
            comp = occurence(noStars,'.')
            pack = occurence(pl[j],'.')
            pack = pack[0:len(comp)]
            if comp == pack:
                print("Packet: " + addr[j] + " is forwarded to interface " + key)
                break

def printFWDTable(fwd):
    width = 35
    title = "Forwarding Table"
    print(f"{title:^{width}}")
    print("**************************************")
    for key ,value in fwd.items():
        print(f"{value}: {key}")
    print("**************************************")
if __name__ == '__main__':
    forwarding_table = make_request(url1,"FT")
    packet_list = make_request(url2,"Packet")
    addresses = make_request(url2,"SaveAddresses")
    printFWDTable(forwarding_table)
    comparingFWDtable(forwarding_table,packet_list,addresses)





# See PyCharm help at https://www.jetbrains.com/help/pycharm/