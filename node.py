import socket
import threading
import json
import rsa
import time
from Blockchain import Blockchain as gbc

def sending(data, nodes_to_connect):
    for i in range(len(nodes_to_connect)):
        ip,port = nodes_to_connect[i].split(":")
        user.sendto(data, (ip,port))

def msg_handle(msg_type, data, b,addr):
    if msg_type == 'blockchain/check':
        ori_len = len(b.chain)
        rec_len = len(data)
        if ori_len < rec_len:
            b.stop_mining = True
            print('Recieved longer blockchain!')
            b.chain = data
            print('Succesfully changed blockchain! Resuming mining...')
            b.stop_mining = False
            sending(MESSAGE_STANDART_3.format(MSG_TYPE='blockchain/check', DATA=b.chain), NODES_TO_CONNECT)
        elif ori_len > rec_len:
            sending(MESSAGE_STANDART_3.format(MSG_TYPE='blockchain/check', DATA=b.chain), NODES_TO_CONNECT)
        elif ori_len == rec_len:
            pass
    elif msg_type == 'block/send':
        if data['previous_hash'] == b.hash(b.last_block()):
            b.stop_mining = True
            print('Recieved suitable block! Apending to blockchain...')
            b.chain.append(data)
            print('Succesfully apended! Resuming mining...')
            b.stop_mining = False
        elif data['previous_hash'] != b.hash(b.last_block()):
            sending(MESSAGE_STANDART_3.format(MSG_TYPE='blockchain/check', DATA=b.chain),NODES_TO_CONNECT)
    elif msg_type == 'transaction/create':
        print('Recieved a transaction.')
        r_tx,sign,s_tx = data
        try:
            rsa.verify(r_tx,sign,s_tx['sender'])
        except rsa.pkcs1.VerificationError:
            print('Recieved transaction is invalid!')
        finally:
            print('Recieved transaction is valid!')
            sending(MESSAGE_STANDART_3.format(MSG_TYPE='transaction/add', DATA=s_tx), NODES_TO_CONNECT)
    elif msg_type == 'connect':
        NODES_TO_CONNECT.append(addr)
        ip,port = addr.split(":")
        user.sendto(MESSAGE_STANDART_3.format(MSG_TYPE='accept'), (ip,port))
        print(addr, 'has been connected.')



def listen_for_messages(bl):
    while True:
        (message,addr) = user.recvfrom(1024)
        message = message.decode()
        if not message:
            continue 
        msg_type , data, standart = message.split('___')
        if standart != 'MST_3':
            if NON_STANDARTIZED_MESSAGE_OUTPUT:
                print('Recieved non standardized message')
                print(message)
                continue
            else:
                continue
        else:
            msg_handle(msg_type,data,bl,addr)



blockchain = gbc()
user = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
with open('node_config.json', 'r') as cfg:
    data = json.load(cfg)
    NODES_TO_CONNECT = data['PRIORITY_NODES']
    NON_STANDARTIZED_MESSAGE_OUTPUT = bool(data['NON_STANDARTIZED_MESSAGE_OUTPUT'])
    ADDR = data['IP_ADDRESS']
    PORT = data['PORT']
MESSAGE_STANDART_3 = '{MSG_TYPE}___{DATA}___MST_3'
user.bind((ADDR,PORT))
print("Started node on",ADDR+":"+str(PORT))
for i in range(len(NODES_TO_CONNECT)):
    addr, port = NODES_TO_CONNECT[i].split(':')
    user.sendto(MESSAGE_STANDART_3.format(MSG_TYPE='connect'), (addr,port))
    data = user.recv(1024)
    if data.startswith('accept'):
        print("Succesfully connected to node", NODES_TO_CONNECT[i])
    else:
        print("Couldn't connect to node", NODES_TO_CONNECT[i])
        NODES_TO_CONNECT.pop(i)
t = threading.Thread(target=listen_for_messages, args=(blockchain,))
t.daemon = True
t.start()