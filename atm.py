import requests

ATM = 'https://giromilano.atm.it/proxy.ashx?lang=it'
SEARCHURL = 'tpPortal/tpl/stops/search/'
GEODATAURL = 'tpPortal/geodata/pois/'

def searchStop(input):
    r = requests.post(ATM, data=buildData(SEARCHURL,input))

    if (r.status_code == 200):
        return r.json()
    else:
        return []


def getWaitingTime(stopNum):
    r = requests.post(ATM, data=buildData(GEODATAURL, stopNum))

    if (r.status_code == 200):
        return r.json()
    else:
        return []

def buildData(url, param):
    return {'url': url + param}
