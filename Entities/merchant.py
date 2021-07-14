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

    def calculate_basket_price(self, basket):
        total = 0
        for item in basket:
            total += self.prices[item]
        return total

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
            response = {'payment_id': payment_id, 'cost': cost}
        return response
