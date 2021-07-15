from Entities import *
from Entities.bank import Bank
from Entities.exchange import Exchange
from Entities.merchant import Merchant
from Entities.user import User
import time

def main():
    user = User()
    merchant = Merchant()
    bank = Bank()
    exchange = Exchange()
    time.sleep(0.3)
    user.create_wallet()
    user.create_bank_account()
    merchant.create_bank_account()
    print(user.buy_basket({'apple': 2}))


if __name__ == '__main__':
    main()
