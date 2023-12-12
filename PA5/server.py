import Cryptodome
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
import socket
def generate_MAC(message, secret):
    message_secret = message + secret
    hashed_message = hashlib.sha256(message_secret.encode()).hexdigest()
    return hashed_message

def decrypt_Message(ciphertext, key):
    block_cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_message = unpad(block_cipher.decrypt(ciphertext), 16)
    return decrypted_message.decode()

def main():
    host = 'localhost'
    port = 9000
    secret = "csci466"
    key = "0123456789ABCDEF"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.bind((host, port))
        c.listen()
        print("Server is listening on port", port)
        conn, addr = c.accept()
        with conn:
            print("Connected by", addr)
            encrypted_message = conn.recv(1024)
            decrypted_message = decrypt_Message(encrypted_message, key)
            received_mac = conn.recv(1024).decode()
            calculated_mac = generate_MAC(decrypted_message, secret)
            if received_mac == calculated_mac:
                print("Accepted, Message is chill like that")
                print("Decrypted Message:", decrypted_message)
            else:
                print("Rejected: Message is SUS ASF.")

if __name__ == "__main__":
    main()