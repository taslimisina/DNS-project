from Connection.client_connection import send_msg


class User:
    def __init__(self):
        self.bank_id = None
        self.wallet_id = None
        self.username = 'uusername'
        self.password = 'upassword'

    def create_bank_account(self):
        msg = {'method': 'signup', 'username': self.username, 'pass_hash': self.password}
        resp = send_msg(msg, 2020)
        if 'error' not in resp:
            self.bank_id = resp['acc_id']

    def create_wallet(self):
        msg = {'method': 'signup', 'username': self.username, 'pass_hash': self.password}
        resp = send_msg(msg, 2040)
        if 'error' not in resp:
            self.wallet_id = resp['acc_id']

    def buy_basket(self, basket):
        msg = {'method': 'buy', 'basket': basket, 'address': 'Tehran'}
        resp = send_msg(msg, 2030)
        if 'error' not in resp:
            cost = resp['cost']
            payment_id = resp['payment_id']
            destination = resp['merchant_id']
            msg = {'method': 'delegate', 'cost': cost, 'username': self.username,
                   'pass_hash': self.password, 'bank_id': 1}
            resp = send_msg(msg, 2040)
            if 'error' not in resp:
                transaction_id = resp['transaction_id']
                msg = {'method': 'transfer', 'payment_id': payment_id, 'destination': destination,
                       'transaction_id': transaction_id, 'cost': cost}
                resp = send_msg(msg, 2020)
        return resp

