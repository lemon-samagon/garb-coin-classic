import socket
import select
import errno
import sys

HOST: str = "127.0.0.1"
PORT: int = 3333
HEADER_LENGTH: int = 10

nodename = input("Node name: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(False)
client_socket.connect((HOST, PORT))

nodename = nodename.encode('utf-8')
nodename_header = f"{len(nodename):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(nodename_header + nodename)

while True:
    scmd = input("> ")

    if scmd:
        scmd = scmd.encode('utf-8')
        scmd_header = f"{len(scmd):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(scmd_header + scmd)
    
    try:
        while True:

            nodename_header = client_socket.recv(HEADER_LENGTH)


            if not len(nodename_header):
                print('Connection closed by the server')
                sys.exit()
            
            nodename_leng = int(nodename_header.decode('utf-8').strip())

            nodename = client_socket.recv(nodename_leng).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Error: {}'.format(str(e)))
            sys.exit()

        continue

    except Exception as e:
        print('Error: '.format(str(e)))
        sys.exit()