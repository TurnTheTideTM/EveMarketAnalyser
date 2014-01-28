__author__ = 'RV Administrator'

from OrderBook import *
from collections import defaultdict

#class Item(object):
#    def __init__(self):
#        self.id = -1
#        self.buyorders = []  # Eine Liste, die Dictionaries im Stil von {ort: preis} enthaelt. Nur die aktuellen.


class TradingBook:
    def __init__(self):
        self._idToOrders = defaultdict(lambda: [OrderBook(Mode.BUY), OrderBook(Mode.SELL)])
        
    def setItem(self, itemId, orderBookB, orderBookS):            
        self._idToOrders.update({itemId: [orderBookB, orderBookS]})

    def getItem(self, itemId):
        """
        Returns the assciated order and buy book.
        """
        return self._idToOrders.get(itemId)[:]  # shallowcopy of what is in the list
        
    def getBuyOrderBook(self, itemId):
        return self._idToOrders.get(itemId, {})[0]
    
    def getSellOrderBook(self, itemId):
        return self._idToOrders.get(itemId, {})[1]
