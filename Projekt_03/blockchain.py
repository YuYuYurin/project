import json
import hashlib
import time
from user import User
from transaction import Transaction


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=100)  # Genesis block

        with open('/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_02/user_data.json', 'r', encoding='utf-8') as file:
            self.users = json.load(file)
        

    def create_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': [transaction.to_dict() for transaction in self.current_transactions],
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block


    def new_transaction(self, user, activity, coins, approver):
        transaction = Transaction(user.name, activity, coins, approver)
        self.current_transactions.append(transaction)
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def confirm_transaction(self, transaction_id, approver):
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['timestamp'] == transaction_id and transaction['approver'] == approver:
                    transaction['confirmed'] = True
                    return True
        return False

    def proof_of_authority(self, user, activity, coins, approver):
        if approver not in [u['name'] for u in self.users if u['role'] == 'parent']:
            raise ValueError("approver is not a parent")
        self.new_transaction(user, activity, coins, approver)
        self.create_block(proof=0)  # Einfacher Proof, da wir PoA verwenden
        return True

    def list_unconfirmed_transactions(self):
        transactions = [transaction.to_dict() for transaction in self.current_transactions]
        return transactions