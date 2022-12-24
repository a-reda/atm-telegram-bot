import requests

ATM = 'https://giromilano.atm.it/proxy.ashx?lang=it'
SEARCHURL = 'tpPortal/tpl/stops/search/'
GEODATAURL = 'tpPortal/geodata/pois/'

headers = { 'Referer': 'https://giromilano.atm.it/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' }

def searchStop(input):
    r = requests.post(ATM, data=buildData(SEARCHURL,input), headers=headers)
    
    if (r.status_code == 200):
        return r.json()
    else:
        return []


def getWaitingTime(stopNum):
    r = requests.post(ATM, data=buildData(GEODATAURL, stopNum), headers=headers)

    if (r.status_code == 200):
        return r.json()
    else:
        return []

def buildData(url, param):
    return {'url': url + param}
