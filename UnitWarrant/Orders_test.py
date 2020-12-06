from MarketData import data, stkcontract, unitcontract, warrantcontract
from contracts import contracts

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order_condition import Create, OrderCondition
from ibapi.order import *

import threading
import time
import copy



class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_details = {}  # Contract details will be stored here using reqId as a dictionary key
        self.openorder_details = {}

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining,
              'lastFillPrice', lastFillPrice)
        self.openorder_details[orderId] = {'status:': status, 'filled': filled, 'remaining': remaining,
              'lastFillPrice': lastFillPrice}

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)
        del self.openorder_details[orderId]

    def contractDetails(self, reqId: int, contractDetails):
        self.contract_details[reqId] = contractDetails

    def get_contract_details(self, reqId, contract):
        self.contract_details[reqId] = None
        self.reqContractDetails(reqId, contract)
        # Error checking loop - breaks from loop once contract details are obtained
        for err_check in range(50):
            if not self.contract_details[reqId]:
                time.sleep(0.1)
            else:
                break
        # Raise if error checking loop count maxed out (contract details not obtained)
        if err_check == 49:
            raise Exception('error getting contract details')
        # Return contract details otherwise
        return app.contract_details[reqId].contract

def run_loop():
    app.run()

def sendorder(contract, price, action, quantity):
    # Create order object
    order = Order()
    order.action = action
    order.totalQuantity = quantity
    order.orderType = 'LMT'
    order.lmtPrice = price
    order.transmit = True

    app.placeOrder(app.nextorderId, contract, order)
    app.openorder_details[app.nextorderId] = {}

app = IBapi()
app.connect('127.0.0.1', 7497, 123)

app.nextorderId = None

# Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

def main(orders,data):
    print(data)
    for ticker in contracts :
        # Check if the API is connected via orderid
        while True:
            if isinstance(app.nextorderId, int):
                print('connected')
                break
            else:
                print('waiting for connection')
                time.sleep(1)

        quantity = -1

        l = [data[ticker.stockreqId]['BID_SIZE'], data[ticker.warrantreqId]['BID_SIZE'], data[ticker.unitreqId]['ASK_SIZE']]

        for x in l:
            if quantity == -1:
                quantity = x
            elif x < quantity:
                quantity = x

        x = 10 #test quantity

        spread = (((data[ticker.stockreqId]['BID'] * 3) + data[ticker.warrantreqId]['BID']) - (data[ticker.unitreqId]['ASK'] * 3))

    #    if (spread > 0.05) and (0 not in l) and (data[ticker.stockreqId]['BID'] > 0) and (data[ticker.warrantreqId]['BID'] > 0) and (data[ticker.unitreqId]['ASK'] > 0):
        if True:
            print("calculation: " + str(data[ticker.stockreqId]['BID']*3) +"+" + str(data[ticker.warrantreqId]['BID']) +"-"+ str(data[ticker.unitreqId]['ASK'] * 3) + "= Spread: " + str(spread))
            sendorder(ticker.stkcontract, data[ticker.stockreqId]['BID'], "SELL", quantity//3)
            app.reqAllOpenOrders()
            print(app.openorder_details)
            orders[ticker.stkcontract.symbol] = app.openorder_details[app.nextorderId]
            app.nextorderId += 1
            sendorder(ticker.unitcontract, data[ticker.unitreqId]['ASK'], "BUY", quantity)
            #orders.append(copy.copy(app.nextorderId))
            app.nextorderId += 1
            sendorder(ticker.warrantcontract, data[ticker.warrantreqId]['BID'], "SELL", quantity//3)
            #orders.append(copy.copy(app.nextorderId))
            app.nextorderId += 1
    return (orders)
orders = {}
while True:
    orders = main(orders,data)
    if orders != {}:
        app.reqOpenOrders()
        orders[stkcontract.symbol] = app.openorder_details[app.nextorderId]
        orders[stkcontract.symbol]['status:']
        print(orders[stkcontract.symbol]['status:'])
        if orders[stkcontract.symbol]['status:'] == "Filled":
            del orders[stkcontract.symbol]
    time.sleep(1)