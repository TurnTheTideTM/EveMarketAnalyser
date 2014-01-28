__author__ = 'RV Administrator'

from .OrderBook import OrderBook, Mode

#class Item(object):
#    def __init__(self):
#        self.id = -1
#        self.buyorders = []  # Eine Liste, die Dictionaries im Stil von {ort: preis} enthält. Nur die aktuellen.

class TradingBook:
    def __init__(self):
        self._idToOrders = {}
        
    def setItem(self, itemId, orderBookB, orderBookS):
        if orderBookB is None or orderBookB.getMode() == Mode.SELL:
            orderBookB = OrderBook(Mode.BUY) # neues buy order book generieren
            
        if orderBookS is None or orderBookS.getMode() == Mode.BUY:
            orderBookS = OrderBook(Mode.SELL) # neues buy order book generieren
            
        self._idToOrders.update({itemId: [orderBookB, orderBookS]})
        
    '''
    Returns the assciated order and buy book.
    '''
    def getItem(self, itemId):
        if itemId not in self._idToOrders.keys():
            orderB = OrderBook(Mode.BUY)
            orderS = OrderBook(Mode.SELL)
            self._idToOrders.update({itemId: [orderB, orderS]})
        return self._idToOrders.get(itemId)[:] ## shallowcopy of what is in the list
        
    def getBuyOrderBook(self, itemId):
        return self._idToOrders.get(itemId, {}).get('b', OrderBook())