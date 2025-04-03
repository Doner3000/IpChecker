import csv
import json
import requests


apikey = open("./api.txt", "r")
print(apikey.read())
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

def processIPsAbuseDB(iparr, apikey):
    resultsAbuseIP = []
    for ip in iparr:
        resultsAbuseIP.append(makeRequestAbuse(ip, apikey))

    #Formatted output
    decodedresponse = json.loads(response.text)
    print(json.dumps(decodedresponse, sort_keys=True, indent=4))

def makeRequestAbuse(ipadd, apikey):
    url = "https://api.abuseipdb.com/api/v2/check"
    querystring = {
        'ipAddress': ipadd,
        'maxAgeInDays': '180'
    }
    headers = {
        'Accept': 'application/json',
        'Key': apikey
    }
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    return response

if __name__ == '__main__':
    processIPsAbuseDB(processCSV(), "2238667a2965c83853805f1e8785afe0ae4dec3bc946f9efcb04e32dce917c7add0fb54207b896d4")
