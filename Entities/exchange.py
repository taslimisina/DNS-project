import time


class Delegation:
    def __init__(self, cost, user_account, bank_id):
        self.cost = cost
        self.user_account = user_account
        self.bank_id = bank_id
        self.timestamp = time.time()


class Exchange:
    def __init__(self):
        self.accounts = {}
        self.passwords = {}
        self.balances = {}
        self.delegations = []
        self.last_id = 0
        self.convert_ratio = 10

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

    def check_pass(self, username, pass_hash):
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
        username = msg['username']
        pass_hash = msg['pass_hash']
        cost = msg['cost']
        bank_id = msg['bank_id']
        acc_id = self.check_pass(username, pass_hash)
        if acc_id:
            delegation = Delegation(cost, acc_id, bank_id)
            self.delegations.append(delegation)
            response = {}
        else:
            response = {'error': 'username or password invalid'}
        return response

