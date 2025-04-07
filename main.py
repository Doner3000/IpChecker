import csv
import json
import os.path
from operator import contains

import requests
import re


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
        ipreader.__next__()
        for row in ipreader:
            csvarr.append(row[0])
            csvarr.append(row[1])
        processIPArray(csvarr)

def processIPArray(iparrinput):
    # Use list comprehension to filter out private IPs
    filtered_ips = [ip for ip in iparrinput if not re.search("(10.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|192\\.168\\.[0-9]{1,3}\\.[0-9]{1,3}|172\\.([1][6-9]|[2][0-9]|[3][0-2])\\.[0-9]{1,3}\\.[0-9]{1,3}|127\\.0\\.0\\.1|0\\.0\\.0\\.0|169\\.254\\.[0-9]{1,3}\\.[0-9]{1,3}|8\\.8\\.8\\.8|8\\.8\\.4\\.4|1\\.1\\.1\\.1)", ip)]
    print(filtered_ips)
    return filtered_ips

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

def checkIfApiKeyLocationIsKnown():
    if not os.path.exists("./api.txt"):
        print("\033[91mThe Api key has not been found.\033[0m")
        match input("What would you like to do now?\n"
                    "Type 1 to add an AbuseIPDB api key and save it to current directory under \"api.txt\"\n"
                    "Type 2 to provide a path to an AbuseIPDB api key and copy it to the current directory under \"api.txt\"\n"
                    "Type 3 to add an AbuseIPDB api key without saving it\n"
                    "Type 4 to exit\n"):
            case "1":
                apikeymanualkeyinput = input("Type the api key into the console:\n")
                with open("./api.txt", "w") as file:
                    file.write(apikeymanualkeyinput)
                    return True
            case "2":
                apikeymanualpathinput = input("Type the path to the api key into the console (without quotes):\n")
                with open(apikeymanualpathinput, "r") as readfile:
                    apikeytemp = str(readfile.read())
                    print(apikeytemp)
                    with open("./api.txt", "w") as writefile:
                        writefile.write(apikeytemp)
                return True
            case "3":
                pass
            case "4":
                exit(1)
    else:
        print("\033[92mKey found. Continuing...\033[0m")

def readKeyFromFile():
    apikey = open("./api.txt", "r")
    return apikey

if __name__ == '__main__':
    print("IpChecker v0.1\n\n")
    if checkIfApiKeyLocationIsKnown():
        print("\033[92mKey added. Enjoy no warnings (hopefully) anymore! <3\033[0m")
    else:
        print("dupa")
    #processCSV()
    #processIPsAbuseDB(processCSV(), apikey.read())
    #apikey.close()
    print("madeit")
    exit()