from . import trader
from . import printeragent

def trader_node():
    trader.Trader().spin()

def print_node():
    printeragent.PrinterAgent().spin()
