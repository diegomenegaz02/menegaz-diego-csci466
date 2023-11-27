import socket
import sys
import time
import random

def send_token(port, token):
    # Seperate to avoid confusion is a common topic
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connect:
        connect.sendto(token.encode(), ('localhost', port))

def rec_token(port):
    # Same Idea ^
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connect:
        connect.bind(('localhost', port))
        data, addr = connect.recvfrom(1024)
        return data.decode()

def maybe_add_to_buffer(num, probability):
    # pbv
    if random.random() < probability:
        num = num + 1

def join_ring(send_port, rec_port, num_packets_to_send, is_head, node_number):

    if is_head:
        # Base Case & has to start it
        while True:
            print(f"Node {node_number}: I have the token! Sending packet out to the internet...")
            maybe_add_to_buffer(num_packets_to_send, 0.25)
            send_token(send_port, "TOKEN")
            num_packets_to_send = num_packets_to_send - 1
            token = rec_token(rec_port)
            if len(token) != 0:
                if num_packets_to_send > 0:
                    # I have packets to send
                    print(f"Node {node_number}: Sending packet out to the internet...")
                    num_packets_to_send = num_packets_to_send - 1
                    maybe_add_to_buffer(num_packets_to_send, 0.25)
                    send_token(send_port, token)
                else:
                    # nothing to send
                    print(f"Node {node_number}: I have nothing to send... sending token to the next node")
                    send_token(send_port, token)
                    maybe_add_to_buffer(num_packets_to_send, 0.25)
            time.sleep(1)
    else:
        # probably could have removed this and made it a seperate function but that kept breaking
        while True:
            token = rec_token(rec_port)
            if len(token) != 0:
                if num_packets_to_send > 0:
                    # I have packets to send
                    print(f"Node {node_number}: Sending packet out to the internet...")
                    num_packets_to_send = num_packets_to_send - 1
                    maybe_add_to_buffer(num_packets_to_send, 0.25)
                    send_token(send_port, token)
                    token = ""
                else:
                    # I have nothing to send... sending token to the next node
                    print(f"Node {node_number}: I have nothing to send... sending token to the next node")
                    send_token(send_port, token)
                    maybe_add_to_buffer(num_packets_to_send, 0.25)
                    token = ""
            time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("You Entered something in Wrong!!!!")
        sys.exit(1)

    send_port = int(sys.argv[1])
    rec_port = int(sys.argv[2])
    num_packets_to_send = int(sys.argv[3])
    is_head = int(sys.argv[4])
    node_number = int(sys.argv[5])
    if is_head == 0:
        join_ring(send_port, rec_port, num_packets_to_send, True, node_number)
    else:
        join_ring(send_port, rec_port, num_packets_to_send, False, node_number)