from Connection.client_connection import send_msg
from config import *


class User:
    def __init__(self):
        self.bank_id = None
        self.wallet_id = None
        self.username = 'uusername'
        self.password = 'upassword'

    def create_bank_account(self):
        """
        tries to create a bank account and set self.bank_id to the bank id in response
        """
        msg = {'method': 'signup', 'username': self.username, 'pass_hash': self.password}
        resp = send_msg(msg, bank_port)
        if 'error' not in resp:
            self.bank_id = resp['acc_id']

    def create_wallet(self):
        """
        tries to create a wallet and set self.wallet_id to the wallet id in response
        """
        msg = {'method': 'signup', 'username': self.username, 'pass_hash': self.password}
        resp = send_msg(msg, exchange_port)
        if 'error' not in resp:
            self.wallet_id = resp['acc_id']

    def buy_basket(self, basket):
        """
        tries to buy given basket from merchant and returns final response
        """
        msg = {'method': 'buy', 'basket': basket, 'address': 'Tehran'}
        resp = send_msg(msg, merch_port)
        if 'error' not in resp:
            cost = resp['cost']
            payment_id = resp['payment_id']
            destination = resp['merchant_account']
            msg = {'method': 'delegate', 'cost': cost, 'username': self.username,
                   'pass_hash': self.password, 'bank_id': 1}
            resp = send_msg(msg, exchange_port)
            if 'error' not in resp:
                transaction_id = resp['transaction_id']
                msg = {'method': 'transfer', 'payment_id': payment_id, 'destination': destination,
                       'transaction_id': transaction_id, 'cost': cost}
                resp = send_msg(msg, bank_port)
        return resp

