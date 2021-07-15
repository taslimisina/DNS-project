import random
import time
from Connection.server_connection import ServerConnection
from config import *


class Delegation:
    def __init__(self, cost, user_account, bank_id):
        self.cost = cost
        self.user_account = user_account
        self.bank_id = bank_id
        self.timestamp = time.time()

    def is_valid(self):
        """
        checks validity of delegation (delegation deactivates after 10 seconds)
        """
        if self.timestamp >= time.time() - 10:
            return True
        else:
            return False


class Exchange:
    def __init__(self):
        self.accounts = {}
        self.passwords = {}
        self.balances = {}
        self.delegations = {}
        self.last_id = 0
        self.convert_ratio = 10
        ServerConnection(self.process_msg, exchange_port)

    def process_msg(self, msg):
        """
        calls related function based on message method
        returns error if method not found
        """
        method = msg['method']
        if method == 'signup':
            return self.signup(msg)
        elif method == 'delegate':
            return self.delegate(msg)
        elif method == 'use_delegation':
            return self.use_delegation(msg)
        else:
            return {'error': 'method not implemented'}

    def generate_transaction_id(self):
        """
        generates random unique transaction id
        """
        transaction_id = random.randint(0, 100000)
        while transaction_id in self.delegations:
            transaction_id = random.randint(0, 100000)
        return transaction_id

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

    def check_pass(self, username, pass_hash):
        """
        returns account id if username and password correct else returns none
        """
        if username in self.accounts:
            acc_id = self.accounts[username]
            correct_pass = self.passwords[acc_id]
            if pass_hash == correct_pass:
                return acc_id
            else:
                return None
        else:
            return None

    def delegate(self, msg):
        """
        called when delegation message is received and add it to delegation messages if username and password correct
        returns transaction id if everything is okay else returns error
        """
        username = msg['username']
        pass_hash = msg['pass_hash']
        cost = msg['cost'] * self.convert_ratio
        bank_id = msg['bank_id']
        acc_id = self.check_pass(username, pass_hash)
        if acc_id:
            delegation = Delegation(cost, acc_id, bank_id)
            transaction_id = self.generate_transaction_id()
            self.delegations[transaction_id] = delegation
            response = {'transaction_id': transaction_id}
        else:
            response = {'error': 'username or password invalid'}
        return response

    def use_delegation(self, msg):
        """
        called when message wants to use a previously received delegation.
        checks if everything is okay does the reduction and returns ok (empty response) else returns error
        """
        cost = msg['cost'] * self.convert_ratio
        transaction_id = msg['transaction_id']
        if transaction_id in self.delegations and self.delegations[transaction_id].is_valid() \
                and cost == self.delegations[transaction_id].cost \
                and cost <= self.balances[self.delegations[transaction_id].user_account]:
            self.balances[self.delegations[transaction_id].user_account] -= cost
            response = {}
        else:
            response = {'error': 'could not do the transaction'}
        return response

