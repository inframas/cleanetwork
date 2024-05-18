import hashlib
import json
import datetime
from flask import Flask, jsonify, request

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.max_tokens = 1900000000  # Maximum token supply
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        # Check if adding this transaction would exceed the maximum token supply
        total_tokens = sum(tx['amount'] for tx in self.transactions) + amount
        if total_tokens > self.max_tokens:
            return 'Exceeds maximum token supply', 400

        # If not, add the transaction as before
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def get_wallet_balance(self, wallet_address):
        balance = 0
        for block in self.chain:
            for tx in block['transactions']:
                if tx['recipient'] == wallet_address:
                    balance += tx['amount']
                if tx['sender'] == wallet_address:
                    balance -= tx['amount']
        return balance

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender='network', recipient='miner_address', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'New block mined',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction_data = request.get_json()
    required_fields = ['sender', 'recipient', 'amount']
    
    if not all(field in transaction_data for field in required_fields):
        return 'Missing fields', 400
    
    index = blockchain.add_transaction(transaction_data['sender'], transaction_data['recipient'], transaction_data['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    response = {'message': 'The blockchain is valid.'} if is_valid else {'message': 'The blockchain is not valid.'}
    return jsonify(response), 200

@app.route('/wallet_balance/<wallet_address>', methods=['GET'])
def get_wallet_balance(wallet_address):
    balance = blockchain.get_wallet_balance(wallet_address)
    response = {'wallet_address': wallet_address, 'balance': balance}
    return jsonify(response), 200

app.run(host='127.0.0.1', port=5000)
