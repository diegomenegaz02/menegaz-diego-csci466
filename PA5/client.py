import Cryptodome
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
import random
import socket



def generate_MAC(message, secret):
    message_secret = message + secret
    hashed_message = hashlib.sha256(message_secret.encode()).hexdigest()
    return hashed_message

def encrypt_Message(message, key):
    block_cipher = AES.new(key.encode(), AES.MODE_ECB)
    ciphertext = block_cipher.encrypt(pad(message.encode(), 16))
    return ciphertext

def corrupt(message):
    if random.random() <= 0.5:
        index_to_modify = random.randint(0, len(message) - 1)
        modified_char = chr((ord(message[index_to_modify]) + 1) % 256)
        message = message[:index_to_modify] + modified_char + message[index_to_modify + 1:]
    return message

def main():
    host = 'localhost'
    port = 9000
    secret = "csci466"
    key = "0123456789ABCDEF"


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((host, port))
        message = input("Enter your secret Message: ")
        corrupted_message = corrupt(message)
        encrypted_message = encrypt_Message(corrupted_message, key)
        c.sendall(encrypted_message)
        mac = generate_MAC(corrupted_message, secret)
        c.sendall(mac.encode())
        print("H(m+s) and message sent.")

if __name__ == "__main__":
    main()