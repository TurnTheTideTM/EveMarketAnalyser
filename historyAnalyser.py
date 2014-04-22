__author__ = 'RV Administrator'

import cPickle
import numpy as np
from collections import defaultdict


TYPEDICT = cPickle.load(open("Data/Processed/typedict.dict", 'r'))


def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]


def moving_average(a, n=1):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def derivative(data, degree):
    if degree == 1:
        return data[-1] - data[-2]
    else:
        return derivative(data, degree - 1) - derivative(data[:-1], degree - 1)


def nextvalue_legacy(data):
    der1 = derivative(data, 1)
    if der1 / data[-1] > 0.2:
        der1 = data[-1] * 0.2
    elif der1 / data[-1] < -0.2:
        der1 = data[-1] * -0.2
    der2 = derivative(data, 2)
    if der2 / data[-1] > 0.05:
        der2 = data[-1] * 0.05
    elif der2 / data[-1] < -0.05:
        der2 = data[-1] * -0.05
    return data[-1] + der1 + der2


def nextvalue(data, depth=3, cutoff=0.2):
    dervs = [derivative(data, x + 1) for x in range(depth)]
    delta = dervs[0]
    for derv in dervs[1:]:
        if derv > cutoff * delta:
            delta *= 1 + cutoff
        elif derv < -cutoff * delta:
            delta *= 1 - cutoff
        else:
            delta += derv
    if delta < (1 - cutoff) * data[-1]:
        return (1 - cutoff) * data[-1]
    elif delta > (1 + cutoff) * data[-1]:
        return (1 + cutoff) * data[-1]
    else:
        return data[-1] + delta


def un_average(data, result, n=1):
    retvalue = result * n
    while n - 1:
        n -= 1
        retvalue -= data[-n]
    return retvalue


def findvols(data):
    vols = {}
    for typeid in data:
        item = data[typeid]
        buyvol = np.array(item["estbuy"])
        totvol = np.array(item["volume"])
        buy5 = moving_average(buyvol)
        tot5 = moving_average(totvol)
        sell5 = tot5 - buy5
        totnext5 = nextvalue(tot5)
        #totnext = un_average(totvol, totnext5)
        if sell5[-1] > 0 and buy5[-1] > 0:
            vols[typeid] = [totnext5, min(
                round(buy5[-1] / tot5[-1], 4),
                round(1 - buy5[-1] / tot5[-1], 4))]
        else:
            vols[typeid] = [totvol[-1], buyvol[-1] / totvol[-1]]
    return vols


def findprices(data, speed=3):
    prices = {}
    for typeid in data:
        item = data[typeid]
        buyprice = np.array(item["lowprice"])
        sellprice = np.array(item["highprice"])
        buy5 = moving_average(buyprice)
        sell5 = moving_average(sellprice)
        buynext5 = nextvalue(buy5)
        sellnext5 = nextvalue(sell5)
        buynext = (buyprice[-1] * speed + un_average(buy5, buynext5)) / (speed + 1)
        sellnext = (sellprice[-1] * speed + un_average(sell5, sellnext5)) / (speed + 1)
        if buynext > sellnext:
            buynext, sellnext = sellnext, buynext
        prices[typeid] = [sellnext, buynext]
    return prices


def finddeals(data, taxes):
    profits = defaultdict(list)
    vols = findvols(data)
    prices = findprices(data)
    for typeid in data:
        volume = vols[typeid]
        sellprice = prices[typeid][0]
        buyprice = prices[typeid][1]
        profit = (sellprice * (1 - taxes[1]) * (1 - taxes[0]) -
                  (buyprice * (1 + taxes[0]))) \
                 * int(volume[0] * volume[1])
        profits[int(profit)].append(typeid)

    for key in sorted(profits, reverse=True):
        if key < 10 ** 7:
            continue
        for element in profits[key]:
            print "Profit:", "{:,}".format(key),
            buyprice = prices[element][1]
            volume = vols[element]
            percent = round(key / ((buyprice * (1 + taxes[0])) * int(volume[0] * volume[1])) * 100, 2)
            print "("+str(percent)+"%)",
            print "for",
            volumes = vols[element]
            print str(int(volumes[0]*volumes[1]))+"x", TYPEDICT[int(element)]


if __name__ == "__main__":
    taxes = [0.0077, 0.009]
    dataset = cPickle.load(open("Data/Processed/historydata_Loc_10000002.dict", 'r'))
    finddeals(dataset, taxes)


