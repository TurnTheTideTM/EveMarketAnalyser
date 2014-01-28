__author__ = 'RV Administrator'


class Item(object):
    def __init__(self):
        self.name = ""
        self.buyorders = []  # Eine Liste, die Dictionaries im Stil von {ort: preis} enthält.
