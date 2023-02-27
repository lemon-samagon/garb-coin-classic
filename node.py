from urllib.parse import urlparse
from hashlib import sha256 as sha
from flask import Flask, jsonify, request
from uuid import uuid4
from Blockchain.Blockchain import Blockchain
import requests

class Node(object):
    def __init__(self):
        self.nodes = set()
    def register_node(self, addr):
        new_addr = urlparse(addr)
        self.nodes.add(new_addr)
    def check_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.sha(last_block.encode()):
                return False
            if sha(str(block['nonce']).encode()) == sha(str(last_block['nonce']).encode()):
                return False
            last_block = block
            current_index +=1
        return True
    def node_consensus(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.check_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            blockchain.chain = new_chain
            return True
        return False
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()
new_node = Node()


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

 	
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        new_node.register_node(node)

    response = {
        'message': 'New nodes have been added', 	
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

 	
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = new_node.node_consensus()
 	
    if replaced:
        response = {
            'message': 'Your chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Your chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])	
def new_transaction():
    values = request.get_json()
    required = ['sender_addr', 'recipient_addr', 'amount', 'signature']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender_addr'], values['recipient_addr'], values['amount'], values['signature'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block	
    last_proof = last_block['nonce']
    proof = blockchain.mine(last_proof)
    blockchain.new_transaction(
        sender_addr = "0",	
        recipient_addr = node_identifier,
        amount = 1,
        signature = "0"
    )
    blockchain.nonce = proof
    block = blockchain.create_block(blockchain.hash(blockchain.last_block))
 	
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'previous_hash': block['previous_hash'],	
    }	
    return jsonify(response), 200

def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }	
    return jsonify(response), 200

if __name__ == '__main__':	
    app.run(host='0.0.0.0', port=43443)