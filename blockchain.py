import json
import hashlib
import time
from user import User
from transaction import Transaction
import logging

logging.basicConfig(level=logging.DEBUG)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.pending_transactions = []  # Liste für unbestätigte Transaktionen
        self.create_block(previous_hash='1')  # Genesis block

        with open('/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_02/user_data.json', 'r', encoding='utf-8') as file:
            self.users = json.load(file)
        

    def create_block(self, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': [transaction.to_dict() for transaction in self.current_transactions],
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        logging.debug(f"New block created: {block}")
        self.chain.append(block)
        return block


    def new_transaction(self, user_name, activity, coins, approver):
        transaction = Transaction(user_name, activity, coins, approver)
        self.pending_transactions.append(transaction)
        return transaction

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def confirm_transaction(self, transaction_id, approver):
        logging.debug(f"Attempting to confirm transaction with ID: {transaction_id} and approver: {approver}")
        for transaction in self.pending_transactions:
                logging.debug(f"Checking transaction: {transaction.to_dict()}")
                if transaction.timestamp == transaction_id and transaction.approver == approver:
                    transaction.confirm()
                    self.current_transactions.append(transaction) # bestätigte Transaktion in current_transactions hinzufügen
                    self.pending_transactions.remove(transaction) 
                    logging.debug(f"Transaction confirmed: {transaction.to_dict()}")
                    if len(self.current_transactions) > 5:
                        self.create_block() 
                        logging.debug("create_block() is called in confirm_transaction().")   
                    return True
        logging.debug(f"Transaction not found or list 'current_transactions' < 5. Length of current_transactions: {len(self.current_transactions)}")
        return False


    def list_unconfirmed_transactions(self):
        transactions = [transaction.to_dict() for transaction in self.pending_transactions]
        return transactions
    
    def list_confirmed_transactions(self):
        transactions = [transaction.to_dict() for transaction in self.current_transactions]
        return transactions
        