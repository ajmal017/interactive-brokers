#Order edits
#Commision estimate
#Combo order

from contracts import contracts

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.contract import ComboLeg
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

for ticker in contracts:
    leg1 = ComboLeg()
    leg1.conId = ticker.stkcontract.conId
    leg1.ratio = 3
    leg1.action = "SSHORT"
    leg1.exchange = "SMART"

    leg2 = ComboLeg()
    leg2.conId = ticker.unitcontract.conId
    leg2.ratio = 3
    leg2.action = "BUY"
    leg2.exchange = "SMART"

    leg2 = ComboLeg()
    leg2.conId = ticker.warrantcontract.conId
    leg2.ratio = 1
    leg2.action = "SSHORT"
    leg2.exchange = "SMART"

    contract.comboLegs = [leg1, leg2, leg3]

    order = Order()
    order.action = "SELL"
    order.orderType = "LMT"
    order.totalQuantity = 1
    order.lmtPrice = 0.01
    self.placeOrder(self.nextOrderId, contract, order)

# class ComboLeg(Object):
#     def __init__(self):
#         self.conId = 0  # type: int
#         self.ratio = 0  # type: int
#         self.action = ""      # BUY/SELL/SSHORT
#         self.exchange = ""
#         self.openClose = 0   # type: int; LegOpenClose enum values
#         # for stock legs when doing short sale
#         self.shortSaleSlot = 0
#         self.designatedLocation = ""
#         self.exemptCode = -1

# order = Order()
# order.action = action
# order.orderType = "LMT"
# order.totalQuantity = quantity
# order.lmtPrice = limitPrice
# if nonGuaranteed:
#     order.smartComboRoutingParams = []
#     order.smartComboRoutingParams.append(TagValue("NonGuaranteed", "1"))