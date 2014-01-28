"""
Created on 28.01.2014

@author: Carbon
"""


class Mode:
    BUY = 0
    SELL = 1


class OrderBook:
    def __init__(self, mode):
        self._mode = mode # Fuer backreference und zur
                            # Vermeidung von versehentlichen puts
        self.orders = []
        
    def getMode(self):
        return self._mode