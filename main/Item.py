__author__ = 'RV Administrator'

from .OrderBook import OrderBook, Mode
from collections import defaultdict

#class Item(object):
#    def __init__(self):
#        self.id = -1
#        self.buyorders = []  # Eine Liste, die Dictionaries im Stil von {ort: preis} enthält. Nur die aktuellen.

class TradingBook:
    def __init__(self):
        self._idToOrders = defaultdict(lambda: [OrderBook(Mode.BUY), OrderBook(Mode.SELL)])
        
    def setItem(self, itemId, orderBookB, orderBookS):            
        self._idToOrders.update({itemId: [orderBookB, orderBookS]})
        
    '''
    Returns the assciated order and buy book.
    '''
    def getItem(self, itemId):
        return self._idToOrders.get(itemId)[:] ## shallowcopy of what is in the list
        
    def getBuyOrderBook(self, itemId):
        return self._idToOrders.get(itemId, {}).get('b', OrderBook())