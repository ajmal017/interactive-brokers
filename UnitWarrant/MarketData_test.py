from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
import threading
import time
import copy
from contracts import contracts


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        if (tickType in [1, 2, 66, 67]):
            if reqId in self.data.keys():
                self.data[reqId][TickTypeEnum.to_str(tickType)] = price
            else:
                self.data[reqId] = {}
                self.data[reqId][TickTypeEnum.to_str(tickType)] = price

    def tickSize(self, reqId, tickType, size):
        if tickType in [0,3,69,70]:
            if reqId in self.data.keys():
                self.data[reqId][TickTypeEnum.to_str(tickType)] = size

def run():
    app.run()

marketdata = {}

app = TestApp()

app.connect("127.0.0.1", 7497, 0)

api_thread = threading.Thread(target=run, daemon=True)
api_thread.start()

time.sleep(1)  # Sleep interval to allow time for connection to server

app.reqMarketDataType(1)  # switch to delayed-frozen data if live is not available
for ticker in contracts:
    app.reqMktData(ticker.stockreqId, ticker.stkcontract, "", False, False, [])
    app.reqMktData(ticker.unitreqId, ticker.unitcontract, "", False, False, [])
    app.reqMktData(ticker.warrantreqId, ticker.warrantcontract, "", False, False, [])
time.sleep(2)  # Sleep interval to allow time for incoming price data
#app.disconnect()
#data = copy.copy(app.data)
data = app.data
#print(data)
