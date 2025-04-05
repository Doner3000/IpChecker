import csv
import json
import requests


apikey = open("./api.txt", "r")

class CheckedIpAbuse:
    def __init__(self, ip, whiteliststatus, abuseconfidence, country, usagetype, isp, domain, istor, totalreports, lastreportdate):
        self.ip = ip
        self.whiteliststatus = whiteliststatus
        self.abuseconfidence = abuseconfidence
        self.country = country
        self.usagetype = usagetype
        self.isp = isp
        self.domain = domain
        self.istor = istor
        self.totalreports = totalreports
        self.lastreportdate = lastreportdate

#source IP is always an even number
def menu(choice):
    print("coming soon")

def processCSV():
    csvpath = input("Please provide the path to csv file: ")
    csvarr = []
    with open(csvpath, newline="") as csvfile:
        ipreader = csv.reader(csvfile, delimiter=",")
        for row in ipreader:
            csvarr.append(row[0])
            csvarr.append(row[1])
            return csvarr

def processIPsAbuseDB(iparr, apikeyreadable):
    resultsabuseip = []
    for i in range(len(iparr)):
        ip = iparr[i]
        jsondoc = makeRequestAbuse(ip, apikeyreadable)
        runningip = jsondoc['data']['ipAddress']
        runningwhitelist = jsondoc['data']['isWhitelisted']
        runningabuseconfidence = jsondoc['data']['abuseConfidenceScore']
        runningcountry = jsondoc['data']['countryCode']
        runningusagetype = jsondoc['data']['usageType']
        runningisp = jsondoc['data']['isp']
        runningdomain = jsondoc['data']['domain']
        runningistor = jsondoc['data']['isTor']
        runningtotalreports = jsondoc['data']['totalReports']
        runninglastreport = jsondoc['data']['lastReportedAt']
        resultsabuseip.append(CheckedIpAbuse(runningip, runningwhitelist, runningabuseconfidence, runningcountry, runningusagetype, runningisp, runningdomain, runningistor, runningtotalreports, runninglastreport))
    print(resultsabuseip[0].abuseconfidence)

#    print(json.dumps(decodedresponse, sort_keys=True, indent=4))

def makeRequestAbuse(ipadd, apikeyreadablerequest):
    url = "https://api.abuseipdb.com/api/v2/check"
    querystring = {
        'ipAddress': ipadd,
        'maxAgeInDays': '180'
    }
    headers = {
        'Accept': 'application/json',
        'Key': apikeyreadablerequest
    }
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    decodedresponse = json.loads(response.text)
    return decodedresponse

if __name__ == '__main__':
    processIPsAbuseDB(processCSV(), apikey.read())
    apikey.close()
