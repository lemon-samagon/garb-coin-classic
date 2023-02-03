# -*- coding: utf-8 -*-

from hashlib import sha256
import json
import time
import os
import random
try:
    import ctypes
except:
    pass #Welcome, Linux
class Blockchain(object):
    def __init__(self):
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass #Hello, Linux
        self.chain = []
        self.current_transactions = []
        self.__nonce = 0
        self.difficulty = 6 #6 = 180.5 MH, 5 = 1 MH, 4 = 45.1 KH
        self.difficulty2 = 100
        self.valid1 = "0"
        if not os.path.exists("blockchainGBC/1.json"):
            self.__create_block(1)
        self.sync()
    def mine(self):
        self.valid1 = "0"
        self.valid2 = "0"
        prv_hash = self.hash(self.last_block)
        print("\033[37mMining started...")
        hashes = 0
        all_hashes = 0
        seconds = int(time.time())
        timeforblock = seconds
        while self.valid1[:self.difficulty] != "0" * self.difficulty:
            self.__nonce = random.randint(1, "9" * self.difficulty2)
            self.__nonce = str(self.__nonce)
            self.valid1 = sha256((prv_hash).encode())
            self.valid2 = self.valid1.update(self.__nonce.encode())
            self.valid1 = str(self.valid1.hexdigest())
            self.__nonce = int(self.__nonce)
            hashes += 1
            all_hashes += 1
            if seconds + 10 == int(time.time()):
                hashrate = hashes // 10 // 1000
                print("\033[34mHashrate: {}KH/s".format(hashrate))
                hashes = 0
                seconds = int(time.time())
        print("\033[33m\033[2mNonce has been founded!")
        print("\033[33mNonce: {0} \nResult: {1}".format(self.__nonce, self.valid1))
        print("\033[33mTotal hashes: {}".format(all_hashes))
        print("\033[33mTotal time: {} seconds".format(time.time() - timeforblock))
        self.valid1 = "0"
        self.valid2 = "0"
        self.__create_block(self.hash(self.last_block))
    def __create_block(self,previous_hash=None):
        if os.path.exists("blockchainGBC/1.json"):
            self.__nonce = str(self.__nonce)
            self.valid1 = sha256((previous_hash).encode())
            self.valid2 = self.valid1.update(self.__nonce.encode())
            self.valid1 = str(self.valid1.hexdigest())
            self.__nonce = int(self.__nonce)
        if self.valid1[:self.difficulty] == "0" * self.difficulty or not os.path.exists("blockchainGBC/1.json"):
            self.__nonce = int(self.__nonce)
            block = {
                'index': len(self.chain) + 1,
                'timestamp': time.time(),
                '__nonce' : self.__nonce,
                'transactions': self.current_transactions,
                'previous_hash': previous_hash or self.hash(self.chain[-1]),
            }
            self.block = block
            self.current_transactions = []
            blockchaindata_dir = 'blockchainGBC'
            filename = '%s/%s.json' % (blockchaindata_dir, self.block['index'])
            with open(filename, 'w') as block_file:
                json.dump(self.block, block_file, indent=5)
            self.chain.append(block)
            print("\033[32mSuccsesfuly apended block to the blockchain!")
        else:
            print("\033[31mInvalid proof of work")
        self.__nonce = 0
    def new_transaction(self, sender_addr, recipient_addr, amount, signature):
        valid = sha256(signature.encode()).hexdigest()
        if valid == sender_addr:
            self.current_transactions.append({
                'sender': sender_addr,
                'recipient': recipient_addr,
                'amount': amount,
            })
            print("\03332mSuccesful transaction!")
            return self.last_block['index'] + 1
        else:
            print("\033[31mInvalid signature or sender addres")
    def sync(self):
        for filename in os.listdir("blockchainGBC"):
            if filename.endswith('.json'):
                filepath = '%s/%s' % ("blockchainGBC", filename)
                with open(filepath, 'r') as block_file:
                    block_info = json.load(block_file)
                    self.chain.append(block_info)
        return self.chain
    def difficulty_update(self):
        self.sync()
        last_block_info = self.last_block()['timestamp']
        first_block_info = (self.chain[-2048])['timestamp']
        block_time = last_block_info - first_block_info
        average_block_time = block_time // 7
        if block_time > 4300800:
            pass
        elif block_time < 4300800:
            #self.difficulty2 = average_block_time * total_hashrate
            pass
        elif block_time == 4300800:
            pass

    @staticmethod
    def hash(block):    
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    @property
    def last_block(self):
        try:
            return self.chain[-1]
        except:
            return {'index' : 0}

if __name__ == "__main__":
    # Ya znau chto etoi takoe
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass
    input("\033[33m\033[2mThis is a module, please, do not open it manually")
    pass
    