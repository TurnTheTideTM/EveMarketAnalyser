__author__ = 'RV Administrator'

from xml.dom import minidom as dom
import urllib2
import nicedict


def parse(filename):
    resultdict = {}
    xmldoc = dom.parse(filename)
    layer = xmldoc.getElementsByTagName('type')
    for node1 in layer:
        typeid = int(node1.attributes["id"].value)
        resultdict[typeid] = {}
        for node2 in node1.childNodes:
            if node2.nodeName == "#text":
                continue
            resultdict[typeid][str(node2.nodeName)] = {}
            for node3 in node2.childNodes:
                resultdict[typeid][str(node2.nodeName)][str(node3.nodeName)] = float(node3.firstChild.data)
    return resultdict


if __name__ == "__main__":
    reqstring = "http://api.eve-central.com/api/marketstat?usesystem=30002187&typeid=34,35"
    f = open("Data/Raw/test.xml", 'w')
    data = urllib2.urlopen(reqstring).readlines()
    for line in data:
        f.write(line)
    f.close()
    data = parse("Data/Raw/test.xml")
    nicedict.nicedict(data)