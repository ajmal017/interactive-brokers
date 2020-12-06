from ibapi.contract import Contract
import copy

class Tickers():
    def __init__(self):
        self.stkcontract = Contract()
        self.stockreqId = 0
        self.unitcontract = Contract()
        self.unitreqId = 0
        self.warrantcontract = Contract()
        self.warrantreqId = 0

count = 1
contracts = []

apxt = Tickers()

apxt.stkcontract.symbol = "APXT"
apxt.stkcontract.secType = "STK"
apxt.stkcontract.exchange = "SMART"
apxt.stkcontract.currency = "USD"
apxt.stkcontract.primaryExchange = "NASDAQ"
apxt.stockreqId = copy.copy(count)
count += 1

apxt.unitcontract.symbol = "APXTU"
apxt.unitcontract.secType = "STK"
apxt.unitcontract.exchange = "SMART"
apxt.unitcontract.currency = "USD"
apxt.unitcontract.primaryExchange = "NASDAQ"
apxt.unitreqId = copy.copy(count)
count += 1

apxt.warrantcontract.symbol = "APXT"
apxt.warrantcontract.secType = "WAR"
apxt.warrantcontract.exchange = "SMART"
apxt.warrantcontract.currency = "USD"
apxt.warrantcontract.primaryExchange = "NASDAQ"
apxt.warrantcontract.lastTradeDateOrContractMonth = "202609"
apxt.warrantcontract.right = "C"
apxt.warrantcontract.strike = 11.5
apxt.warrantreqId = copy.copy(count)
count += 1

contracts.append(apxt)

lca = Tickers()

lca.stkcontract.symbol = "LCA"
lca.stkcontract.secType = "STK"
lca.stkcontract.exchange = "SMART"
lca.stkcontract.currency = "USD"
lca.stkcontract.primaryExchange = "NASDAQ"
lca.stkreqId = copy.copy(count)
count += 1

lca.unitcontract.symbol = "LCAHU"
lca.unitcontract.secType = "STK"
lca.unitcontract.exchange = "SMART"
lca.unitcontract.currency = "USD"
lca.unitcontract.primaryExchange = "NASDAQ"
lca.unitreqId = copy.copy(count)
count += 1

lca.warrantcontract.symbol = "LCA"
lca.warrantcontract.secType = "WAR"
lca.warrantcontract.exchange = "SMART"
lca.warrantcontract.currency = "USD"
lca.warrantcontract.primaryExchange = "NASDAQ"
lca.warrantcontract.lastTradeDateOrContractMonth = "202605"
lca.warrantcontract.right = "C"
lca.warrantcontract.strike = 11.5
lca.warrantreqId = copy.copy(count)
count += 1

contracts.append(lca)