import config
from Connection.server_connection import ServerConnection
from Connection.client_connection import send_msg
from config import *


class Bank:
    def __init__(self):
        self.id = 1
        self.accounts = {}
        self.passwords = {}
        self.balances = {}
        self.last_id = 0
        ServerConnection(self.process_msg, bank_port)

    def process_msg(self, msg):
        """
        calls related function based on message method
        returns error if method not found
        """
        method = msg['method']
        if method == 'signup':
            return self.signup(msg)
        elif method == 'transfer':
            return self.transfer(msg)
        else:
            return {'error': 'method not implemented'}

    def signup(self, msg):
        """
        called when signup message is received
        returns generated account id if everything is ok else returns error
        """
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
        """
        processes a transfer message tries to sell crypto and send it to merchant account
        returns payment id if everything goes well else everything is reverted and error is returned
        """
        payment_id = msg['payment_id']
        destination = msg['destination']
        transaction_id = msg['transaction_id']
        cost = msg['cost']
        if destination not in self.balances:
            response = {'error': 'destination does not exist'}
        else:
            self.balances[destination] += cost
            msg = {'method': 'use_delegation', 'cost': cost, 'transaction_id': transaction_id}
            resp = send_msg(msg, config.exchange_port)
            if 'error' in resp:
                self.balances[destination] -= cost
                response = {'error': 'problem with exchange'}
            else:
                msg = {'method': 'transaction_done', 'payment_id': payment_id}
                send_msg(msg, config.merch_port)
                response = {'payment_id': payment_id}
        return response

