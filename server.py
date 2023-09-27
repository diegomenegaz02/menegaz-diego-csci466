import sys
import socket
import numpy as pynum
import random
count = 0
board = pynum.array([[0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]])

def Build_Board(array):

    ship4 = pynum.array([1, 1, 1, 1])
    ship3 = pynum.array([1, 1, 1])
    ship2 = pynum.array([1, 1])
    # making sure the boats don't generate out of bounds
    placement1x = random.randint(0, 1)
    placement1y = random.randint(0, 5)
    placement2x = random.randint(0, 2)
    placement2y = random.randint(0, 5)
    placement3x = random.randint(0, 2)
    placement3y = random.randint(0, 5)
    # Handling if they randomly are on the same line
    while (placement1y == placement2y):
        if (placement1y == 0):
            placement2y = random.randing(placement1y, 6)
        else:
            placement2y = random.randint(0, placement1y)
    while (placement1y == placement3y):
        if (placement1y == 0):
            placement3y = random.randint(placement1y, 6)
        else:
            placement3y = random.randint(0, placement1y)
    while (placement2y == placement3y):
        if (placement2y == 0):
            placement3y = random.randint(placement2y, 6)
        else:
            placement3y = random.randint(0, placement2y)


    array[placement1y, placement1x:placement1x + 4] = ship4
    array[placement2y, placement2x:placement2x + 3] = ship3
    array[placement3y, placement2x:placement2x + 2] = ship2
    print(array)

def start_server(port):
    # Create a socket object

    Build_Board(board)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(("0.0.0.0", port))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Listening on port {port}...")
    #Creation of Board
    hasWon = False

    client_socket, client_address = server_socket.accept()
    while True:
        # Accept a connection from a client
        print(f"Accepted connection from {client_address}")
        # Handle the connection (you can add your custom logic here)
        # For demonstration purposes, we'll just echo back messages to the client
        count = 0
        for row in board:
            for num in row:
                if(num == 2):
                    count = count + 1
                    if(count == 9):
                        client_socket.send("WINNER WINNER CHICKEN DINNER".encode())

        user_guess = str(client_socket.recv(1024).decode())
        print(user_guess)
        digits = [int(char) for char in user_guess]
        guessx= digits[0] - 1 #to handle discrempency between array and actual coords
        guessy= digits[1] - 1
        if(board[guessx][guessy] == 1):
            board[guessx][guessy] = 2
            client_socket.send("HIT!".encode())
        elif(board[guessx][guessy] == 2):
            client_socket.send("You have already hit that part of the ship".encode())
        else:
            client_socket.send("MISS".encode())

        print(board)


if __name__ == "__main__":
    sock = int(input("Couldn't get arg to work input socket here\n"))
    if(sock != 8000):
        print("wrong")
    else:
        start_server(sock)


