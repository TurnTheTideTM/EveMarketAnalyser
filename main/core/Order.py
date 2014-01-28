"""
Created on 28.01.2014

@author: Carbon
"""

class Order(object):
    """
    Repraesentiert eine Order im Handel. Speichert eine eigene History 
    """

    def __init__(self, uuid, iniPrize, iniAmout, rangeOO, mode):
        """
        Constructor
        """
        self.range = rangeOO
        self.mode = mode
        self._states = [State(iniPrize, iniAmout)]
        self.snapshotToState = [0]
        
    def __iadd__(self, pMArr):
        if self._states[-1] != pMArr:
            self._states.append(State(pMArr[0], pMArr[1]))
        self.snapshotToState.append(len(self._states) - 1)
        return self
        
    def __getitem__(self, snapshotNbr):
        """
        Wird eine Exception raisen wenn der Zustand nicht existiert / diese Order 'zu jung' ist.
        0 <= snapshotNbr < len(snapshotToState)
        """
        return self._states[self.snapshotToState[snapshotNbr]]
    
    ## def __contains__(self, arr)
        
class State(object):
    """
    Repraesentiert einen state einer Order
    """
    def __init__(self, prize, amount):
        self.preis = prize
        self.menge = amount
        
    def __eq__(self, other):
        if type(other) == type(self):
            return (self.preis == other.preis and
            self.menge == other.menge)
        return [self.preis, self.menge] == other
    
        raise NotImplementedError()
    
    def __str__(self):
        return 'Preis %d, Menge %d' % (self.preis, self.menge)
    
if __name__ == "__main__":
    pass