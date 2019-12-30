from . import trader
from . import printagent

def trader_node():
    trader.Trader().spin()

def print_node():
    printagent.PrintAgent().spin()
