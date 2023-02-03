import socket
import select

HOST: str = "127.0.0.1"
PORT: int = 3333
HEADER_LENGHT: int = 10

serv_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serv_socket.bind((HOST, PORT))
serv_socket.listen()
        

nodes = [serv_socket]
socket_list: dict = {}

def reciver(c_socket):
    try: 
        msg_header: bytes = c_socket.recv(HEADER_LENGHT)
        if not len(msg_header):
            return False
        msg_len: int = int(msg_header.decode('utf-8').strip())
        return {"msg_header": msg_header, "data": c_socket.recv(msg_len)}
    except:
        return False

if __name__ == "__main__":
    while True:
        r_sockets,_,exp_sockets = select.select(socket_list, [], socket_list)

        for n_socket in r_sockets:
            if n_socket == serv_socket:
                c_socket, c_address = serv_socket.accept()

                usr: bytes = reciver(c_socket=c_socket)
                if usr is False:
                    continue

                socket_list.append(c_socket)

                nodes[c_socket] = usr

                print(f"[LOG] New node {c_address[0]}:{c_address[1]} name:{usr['data'].decode('utf-8')}")
            else:
                msg = reciver(n_socket)

                if msg is False:
                    print(f"[LOG] Node {nodes[n_socket]['data'].decode('utf-8')} disconnected")
                    socket_list.remove(n_socket)
                    del nodes[n_socket]
                    continue

                node = nodes[n_socket]
                print(f"[LOG] {nodes[n_socket]['data'].decode('utf-8')}: {msg['data'].decode('utf-8')}")

                """
                for c_socket in nodes:
                    if c_socket != n_socket:
                        c_socket.send()
                """
        
        for n_socket in exp_sockets:
            socket_list.remove(n_socket)
            del nodes[n_socket]
