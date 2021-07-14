
class Bank:
    def __init__(self):
        self.id = 1
        self.accounts = {}
        self.passwords = {}
        self.balances = {}
        self.last_id = 0

    def signup(self, msg):
        initial_balance = 100
        username = msg['username']
        pass_hash = msg['pass_hash']
        acc_id = self.last_id = self.last_id + 1
        self.accounts[username] = acc_id
        self.passwords[acc_id] = pass_hash
        self.balances[acc_id] = initial_balance
        response = {'acc_id': acc_id}
        return response

