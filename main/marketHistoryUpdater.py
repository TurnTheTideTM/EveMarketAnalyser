__author__ = 'RV Administrator'


import urllib2
import json
import datetime
import cPickle


def update(itemlist, location=10000002):
    fullHistory = {}
    total = len(itemlist)
    counter = 1
    for typeid in itemlist:
        print "{0:04d}".format(counter), "/", total, "("+str("{0:05d}".format(typeid))+")",
        counter += 1
        url = "http://public-crest.eveonline.com/market/"+str(location)+"/types/"+str(typeid)+"/history/"
        filepath = "Data/Raw/PriceHistory/pricehistory"+str(typeid)+".json"
        f = open(filepath, 'w')
        data = urllib2.urlopen(url).readlines()
        for line in data:
            f.write(line)
        f.close()
        data = json.load(open(filepath, 'r'))
        if len(data["items"]) < 300:
            print "skipped"
            continue
        try:
            fullHistory[typeid] = process_data(data)
        except:
            print "skipped"
            continue
        print "done"
    cPickle.dump(fullHistory, open("Data/Processed/historydata_Loc_"+str(location)+".dict", 'w'))


def create_full(itemlist, location=10000002):
    fullHistory = {}
    counter = 1
    for typeid in itemlist:
        if counter % 1000 == 0:
            fullHistory.update(cPickle.load(open("Data/Processed/historydata_Loc_"+str(location)+"_C_"+str(counter)+".dict", 'r')))
        counter += 1
    fullHistory.update(cPickle.load(open("Data/Processed/historydata_Loc_"+str(location)+"_C_"+str(counter)+".dict", 'r')))
    return fullHistory


def process_data(data):
    result = {"volume": [],
              "ordercount": [],
              "lowprice": [],
              "highprice": [],
              "avgprice": [],
              "estbuy": []}
    data = data["items"]
    startdate_raw = data[0]["date"].split("T")[0].split("-")
    prevdate = datetime.date(year=int(startdate_raw[0]), month=int(startdate_raw[1]), day=int(startdate_raw[2]))
    for i in data:
        date_raw = i["date"].split("T")[0].split("-")
        date = datetime.date(year=int(date_raw[0]), month=int(date_raw[1]), day=int(date_raw[2]))
        delta = (date - prevdate).days - 1
        if delta > 0:
            for j in xrange(delta):
                result["volume"].append(0)
                result["ordercount"].append(0)
                result["lowprice"].append(0)
                result["highprice"].append(0)
                result["avgprice"].append(0)
                result["estbuy"].append(0)

        volume = int(i["volume"])
        ordercount = int(i["orderCount"])
        lowprice = float(i["lowPrice"])
        highprice = float(i["highPrice"])
        avgprice = float(i["avgPrice"])
        estbuy = 0

        if highprice != lowprice:
            estbuy = round((volume * (highprice - avgprice))/(highprice - lowprice), 2)

        result["volume"].append(volume)
        result["ordercount"].append(ordercount)
        result["lowprice"].append(lowprice)
        result["highprice"].append(highprice)
        result["avgprice"].append(avgprice)
        result["estbuy"].append(estbuy)

        prevdate = date

    return result



if __name__ == "__main__":
    typeids = cPickle.load(open("Data/Processed/activeItems.list", 'r'))
    typeids = [34, 35]
    hub = 10000043
    update(typeids, hub)
    #data = cPickle.load(open("Data/Processed/historydata_Loc_10000043.dict", 'r'))