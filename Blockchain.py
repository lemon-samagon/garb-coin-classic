# -*- coding: utf-8 -*-

from hashlib import sha256
import json
import time
import os
from ecdsa.util import sigencode_der
from ecdsa import SigningKey,BadSignatureError
import random
try:
    import ctypes
except:
    pass 
class Blockchain(object):
    def __init__(self):
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass 
        self.chain = []
        self.current_transactions = []
        self.nonce = 0
        self.difficulty = 6
        self.difficulty2 = 100
        self.valid1 = "0"
        self.stop_mining = False
        if not os.path.exists("blockchainGBC/1.json"):
            self.create_block(1)
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
            if not self.stop_mining:
                self.nonce = random.randint(1, 9 * self.difficulty2)
                self.nonce = str(self.nonce)
                self.valid1 = sha256((prv_hash).encode())
                self.valid2 = self.valid1.update(self.nonce.encode())
                self.valid1 = str(self.valid1.hexdigest())
                self.nonce = int(self.nonce)
                hashes += 1
                all_hashes += 1
                if seconds + 10 == int(time.time()):
                    hashrate = hashes // 10 // 1000
                    print("\033[34mHashrate: {}KH/s".format(hashrate))
                    hashes = 0
                    seconds = int(time.time())
            else:
                time.sleep(0.5)
        print("\033[33m\033[2mNonce has been founded!")
        print("\033[33mNonce: {0} \nResult: {1}".format(self.nonce, self.valid1))
        print("\033[33mTotal hashes: {}".format(all_hashes))
        print("\033[33mTotal time: {} seconds".format(time.time() - timeforblock))
        self.valid1 = "0"
        self.valid2 = "0"


    def create_block(self,previous_hash=None):
        if os.path.exists("blockchainGBC/1.json"):
            self.nonce = str(self.nonce)
            self.valid1 = sha256((previous_hash).encode())
            self.valid2 = self.valid1.update(self.nonce.encode())
            self.valid1 = str(self.valid1.hexdigest())
            self.nonce = int(self.nonce)
        if self.valid1[:self.difficulty] == "0" * self.difficulty or not os.path.exists("blockchainGBC/1.json"):
            self.nonce = int(self.nonce)
            block = {
                'index': len(self.chain) + 1,
                'timestamp': time.time(),
                'nonce' : self.nonce,
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
            self.nonce = 0
            return block
        else:
            print("\033[31mInvalid proof of work")
            self.nonce = 0
            return None


    def new_transaction(self, pub_sender_addr, recipient_addr, amount, prv_sender_key):
        raw_transaction = {'sender': pub_sender_addr,'recipient': recipient_addr,'amount': amount}
        signature = prv_sender_key.sign_deterministic(raw_transaction,hashfunc=sha256, sigencode=sigencode_der)
        signed_transaction = {
            'sender': pub_sender_addr,
            'recipient': recipient_addr,
            'amount': amount,
            'signature' : signature
        }
        self.current_transactions.append(signed_transaction)
        print("\03332mSuccesful transaction!")
        return raw_transaction,signature,signed_transaction

    def verify_signature(self, transaction):
        signature = transaction.pop('signature')
        raw_transaction = transaction
        pub_sender_addr = transaction['sender']
        try:
            ver = pub_sender_addr.verify(signature, raw_transaction, sha256, sigdecode = sigencode_der)
            assert ver
            print('Valid signature')
            return True
        except BadSignatureError:
            print('Invalid signature') 
            return False


    def sync(self):
        for filename in os.listdir("blockchainGBC"):
            if filename.endswith('.json'):
                filepath = '%s/%s' % ("blockchainGBC", filename)
                with open(filepath, 'r') as block_file:
                    block_info = json.load(block_file)
                    self.chain.append(block_info)
        return self.chain

    def recover_chain(self, chain, difficulty):
        self.difficulty = difficulty
        blockchaindata_dir = 'blockchainGBC'
        self.chain = []
        for i in range(len(chain)):
            filename = '%s/%s.json' % (blockchaindata_dir, (chain[i])["index"])
            with open(filename, 'w') as block_file:
                json.dump(chain[i], block_file, indent=5)
            self.chain.append(chain[i])


    def difficulty_update(self):
        self.sync()
        last_block_info = self.last_block()['timestamp']
        first_block_info = (self.chain[-1024])['timestamp']
        block_time = last_block_info - first_block_info
        average_block_time = block_time // 7
        if block_time > 604800:
            self.difficulty -= 1
        elif block_time < 604800:
            self.difficulty += 1

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

    def export_blockchain(self):
        return self.chain, self.difficulty

if __name__ == "__main__":
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass
    input("\033[33m\033[2mThis is a module, please, do not open it manually")
    print("\033[37m")