import socket
import threading
import random
user = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PORT = random.randint(43000,44000)
ADDR = input("Type your ip address: ")
user.bind((ADDR, PORT))
print("Connected as ",ADDR+":"+str(PORT))
def listen_for_messages():
    while True:
        message, addr = user.recvfrom(1024)
        message = message.decode()
        if not message:
            continue
        print("\rFrom: ",addr," Message: ", message,"\n:", end="")

t = threading.Thread(target=listen_for_messages)
t.daemon = True
t.start()
to_addr = None
to_port = None
while True:
    data = input(":")
    if not data:
        break 
    if data.startswith('/connect'):
        cmd, addr = data.split(' ')
        to_addr,to_port = addr.split(":")
    else:
        try:
            user.sendto(data.encode(), (to_addr, int(to_port)))
        except:
            print("No connected users!")