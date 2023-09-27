
import socket

port = 8000
host = socket.gethostname()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))

def run():

    hasSolved = False

    while (not hasSolved):

        user_guess = input("Enter the two digit number of your answer 12 = [1,2]\n")

        clientSocket.send(user_guess.encode())

        response = clientSocket.recv(1024).decode()

        print(response)
        if (response == "WINNER WINNER CHICKEN DINNER"):
            hasSolved = True
        elif (response == "MISS"):
            print("MISS")
        elif(response == "HIT!"):
            print("HIT")
        else:
            print("What happened lol")

if __name__ == "__main__":

    run()