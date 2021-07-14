class User:
    def __init__(self):
        self.bank_id = None
        self.wallet_id = None
        self.username = 'username'
        self.password = 'password'

    def create_bank_account(self):
        msg = {'method': 'signup', 'username': self.username, 'pass_hash': self.password}
        resp = self.send_msg_to_bank(msg)
        if 'error' not in resp:
            self.bank_id = resp['acc_id']

    def create_wallet(self):
        msg = {'method': 'signup', 'username': self.username, 'pass_hash': self.password}
        resp = self.send_msg_to_exchange(msg)
        if 'error' not in resp:
            self.wallet_id = resp['acc_id']

    def buy_basket(self, basket):
        msg = {'method': 'buy', 'basket': basket, 'address': 'Tehran'}
        resp = self.send_msg_to_merchant(msg)
        if 'error' not in resp:
            cost = resp['cost']
            payment_id = resp['payment_id']
            msg = {'method': 'delegate', 'cost': cost, 'username': self.username,
                   'pass_hash': self.password, 'bank_id': 1}
            resp = self.send_msg_to_exchange(msg)
            if 'error' not in resp:
                transaction_id = resp['transaction_id']

