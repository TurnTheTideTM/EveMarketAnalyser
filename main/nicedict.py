__author__ = 'RV Administrator'


def nicedict(data, white = 0, newline = True):
    if type(data) == list:
        for i in data:
            nicedict(i, white+3, False)
    elif type(data) == dict:
        for i in data:
            if type(data[i]) == list or type(data[i]) == dict:
                print " "*white + str(i) + ":"
                nicedict(data[i], white + 3)
            else:
                print " "*white + str(i) + ": " + str(data[i])

    else:
        print " "*white + str(data)
    if newline:
        print