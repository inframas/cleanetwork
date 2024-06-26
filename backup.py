# Python program to create Blockchain

# For timestamp
import datetime

# Calculating the hash
# in order to add digital
# fingerprints to the blocks
import hashlib

# To store data
# in our blockchain
import json

# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify

class Blockchain:

    # This function is created
    # to create the very first
    # block and set its hash to "0"
    def __init__(self):
        self.chain = []
        self.load_chain()

    # Load blockchain from file
    def load_chain(self):
        try:
            with open('blockchain.json', 'r') as file:
                self.chain = json.load(file)
        except FileNotFoundError:
            self.create_block(proof=1, previous_hash='0', transactions=[])  # Provide an empty list of transactions

    # Save blockchain to file
    def save_chain(self):
        with open('blockchain.json', 'w') as file:
            json.dump(self.chain, file)

    # This function is created
    # to add further blocks
    # into the chain
    def create_block(self, proof, previous_hash, transactions):
        block = {'index': len(self.chain) + 1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash': previous_hash,
                'transaction': transactions}
        self.chain.append(block)
        self.save_chain()  # Save after adding block
        return block

    # This function is created
    # to display the previous block
    def print_previous_block(self):
        return self.chain[-1]

    # This is the function for proof of work
    # and used to successfully mine the block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha512(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha512(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha512(
                str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1

        return True

# Creating the Web
# App using flask
app = Flask(__name__)

# Create the object
# of the class blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/create_transactions', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    transactions =       {
        "sender": "sender_address",
        "recipient": "recipient_address",
        "amount": 10,
        "timestamp": "transaction_timestamp",
        "transaction_id": "transaction_identifier",
        "signature": "transaction_signature"
      }
    block = blockchain.create_block(proof, previous_hash, transactions)

    response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}

    return jsonify(response), 200

# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)

    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200

# Run the flask server locally
app.run(host='127.0.0.1', port=5000)
