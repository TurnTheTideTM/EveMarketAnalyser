from main import xmlHandler

__author__ = 'RV Administrator'

import urllib2
import cPickle

alldata = {}


def getdata(typeids=[34, 35], systemid=30002187):
    url = "http://api.eve-central.com/api/marketstat?usesystem="+str(systemid)+"&typeid="
    for typeid in typeids[:-1]:
        url += str(typeid) + ","
    url += str(typeids[-1])
    filepath = "Data/Raw/Prices/data_TypeID"+str(typeids).replace("[", "").replace("]",
                                    "").replace(",", "_")+"_SystemID_"+str(systemid)+".xml"
    f = open(filepath, 'w')
    data = urllib2.urlopen(url).readlines()
    for line in data:
        f.write(line)
    f.close()
    alldata.update(xmlHandler.parse(filepath))


def getbuysell(typeid):
    if typeid in alldata:
        return alldata[typeid]["buy"]["max"], alldata[typeid]["sell"]["min"]


if __name__ == "__main__":
    getdata()
    print getbuysell(34)