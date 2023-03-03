import socket
import threading
import random
user = socket.socket()
user.bind(("", random.randint(43000,44000)))
def listen_for_messages():
    while True:
        message, addr = user.recvfrom(1024).decode()
        print("From: ",addr," Message: ", message)

t = threading.Thread(target=listen_for_messages)
t.daemon = True
t.start()
while True:
    data = input(":")
    user.sendall(data.encode())