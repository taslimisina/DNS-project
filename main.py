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
    resp = user.buy_basket({'apple': 10})
    print("final result")
    print(resp)
    print("user bank account balance")
    print(bank.balances[user.bank_id])
    print("user wallet balance")
    print(exchange.balances[user.wallet_id])
    print("merchant bank balance")
    print(bank.balances[merchant.bank_id])


if __name__ == '__main__':
    main()
