from Connection.server_connection import ServerConnection
from Connection.client_connection import send_msg


class Bank:
    def __init__(self):
        self.id = 1
        self.accounts = {}
        self.passwords = {}
        self.balances = {}
        self.last_id = 0
        ServerConnection(self.process_msg, 20020)

    def process_msg(self, msg):
        method = msg['method']
        if method == 'signup':
            return self.signup(msg)
        elif method == 'transfer':
            return self.transfer(msg)
        else:
            return {'error': 'method not implemented'}

    def signup(self, msg):
        initial_balance = 100
        username = msg['username']
        if username in self.accounts:
            response = {'error': 'username exists'}
        else:
            pass_hash = msg['pass_hash']
            acc_id = self.last_id = self.last_id + 1
            self.accounts[username] = acc_id
            self.passwords[acc_id] = pass_hash
            self.balances[acc_id] = initial_balance
            response = {'acc_id': acc_id}
        return response

    def transfer(self, msg):
        payment_id = msg['payment_id']
        destination = msg['destination']
        transaction_id = msg['transaction_id']
        cost = msg['cost']
        if destination not in self.balances:
            response = {'error': 'destination does not exist'}
        else:
            self.balances[destination] += cost
            msg = {'method': 'use_delegation', 'cost': 'cost', 'transaction_id': transaction_id}
            resp = self.send_msg_to_exchange(msg)
            if 'error' in resp:
                self.balances -= cost
                response = {'error': 'problem with exchange'}
            else:
                msg = {'method': 'transaction_done', 'payment_id': payment_id}
                self.send_msg_to_merchant(msg)
                response = {'payment_id': payment_id}
        return response

