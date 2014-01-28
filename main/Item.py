__author__ = 'RV Administrator'


class Item(object):
    def __init__(self):
        self.id = -1
        self.buyorders = []  # Eine Liste, die Dictionaries im Stil von {ort: preis} enthält. Nur die aktuellen.
