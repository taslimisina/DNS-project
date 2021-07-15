from Connection.server_connection import ServerConnection
from Connection.client_connection import send_msg
from config import *

class Order:
    def __init__(self, basket, address, payment_id, price):
        self.payment_id = payment_id
        self.basket = basket
        self.address = address
        self.price = price


class Merchant:
    def __init__(self):
        self.prices = {'apple': 10, 'banana': 20, 'melon': 30}
        self.orders = {}
        self.last_payment_id = 0
        self.bank_id = None
        self.username = 'musername'
        self.password = 'mpassword'
        ServerConnection(self.process_msg, merch_port)

    def process_msg(self, msg):
        method = msg['method']
        if method == 'buy':
            return self.buy(msg)
        else:
            return {'error': 'method not implemented'}

    def calculate_basket_price(self, basket):
        total = 0
        for item in basket:
            total += self.prices[item] * basket[item]
        return total

    def create_bank_account(self):
        msg = {'method': 'signup', 'username': self.username, 'pass_hash': self.password}
        resp = send_msg(msg, bank_port)
        if 'error' not in resp:
            self.bank_id = resp['acc_id']

    def buy(self, msg):
        basket = msg['basket']
        address = msg['address']
        try:
            cost = self.calculate_basket_price(basket)
        except KeyError:
            response = {'error': 'item not found'}
        else:
            payment_id = self.last_payment_id = self.last_payment_id + 1
            self.orders[payment_id] = Order(basket, address, payment_id, cost)
            response = {'payment_id': payment_id, 'cost': cost, 'merchant_account': self.bank_id}
        return response
