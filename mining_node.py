import socket
import threading
import json
import rsa
from Blockchain import Blockchain as gbc

def mining(b):
    while True:
        b.mine(MINING_SPEED_LIMIT)
        new_block = b.create_block(b.last_block())
        user.send(MESSAGE_STANDART_3.format(MSG_TYPE='block/send', DATA=new_block))


def msg_handle(msg_type, data, b):
    if msg_type == 'blockchain/check':
        ori_len = len(b.chain)
        rec_len = len(data)
        if ori_len < rec_len:
            b.stop_mining = True
            print('Recieved longer blockchain!')
            b.chain = data
            print('Succesfully changed blockchain! Resuming mining...')
            b.stop_mining = False
        elif ori_len > rec_len:
            user.send(MESSAGE_STANDART_3.format(MSG_TYPE='blockchain/check', DATA=b.chain))
        elif ori_len == rec_len:
            pass
    elif msg_type == 'block/send':
        if data['previous_hash'] == b.hash(b.last_block):
            b.stop_mining = True
            print('Recieved suitable block! Apending to blockchain...')
            b.chain.append(data)
            print('Succesfully apended! Resuming mining...')
            b.stop_mining = False
    elif msg_type == 'transaction/add':
        b.stop_mining = True
        print('Recieved a new transaction!')
        b.current_transactions.append(data)
        b.stop_mining = False


def listen_for_messages(bl):
    while True:
        try:
            message = user.recv(1024)
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
                msg_handle(msg_type,data,bl)
        except:
            print("Error while reciving data")


blockchain = gbc()
user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with open('node_config.json', 'r') as cfg:
    data = json.load(cfg)
    PRIORITY_NODES = data['PRIORITY_NODES']
    MINING_SPEED_LIMIT = data['MINING_SPEED_LIMIT']
    NON_STANDARTIZED_MESSAGE_OUTPUT = bool(data['NON_STANDARTIZED_MESSAGE_OUTPUT'])
MESSAGE_STANDART_3 = '{MSG_TYPE}___{DATA}___MST_3'
for i in range(len(PRIORITY_NODES)):
    try:
        print('Trying to connect to',PRIORITY_NODES[i])
        ADDR,PORT = PRIORITY_NODES[i].split(':')
        user.connect((ADDR,PORT))
    except:
        print('Unsuccsesful connection')
print("Connected to ",ADDR+":"+str(PORT))
t = threading.Thread(target=listen_for_messages, args=(blockchain,))
t.daemon = True
t.start()
m = threading.Thread(target=mining, args=(blockchain,))
m.daemon = True
m.start()