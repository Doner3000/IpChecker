import csv
import json
import os.path
import requests
import re


global apikey
global configfile

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

def menu():
    checkIfConfigIsInCurrentDir()
    while True:
        match (input("Hello there, hope you are having a great day!\n"
                "What would you like to do?\n"
                "Type a number corresponding to the option you want to choose:\n\n"
                "1. Check single IP against AbuseIPDB\n"
                "2. Provide a CSV file containing IP addresses and check against AbuseIPDB\n"
                "3. Provide an array of IP addresses and check these against AbuseIPDB\n"
                "9. Settings\n"
                "0. Exit\n")):
            case "1":
                break
            case "2":
                break
            case "3":
                break
            case "9":
                break
            case "0":
                break
            case _:
                print("Response not a valid number, please try again.\n")

def checkIfConfigIsInCurrentDir():
    if not os.path.exists("config.json"):
        print("\033[93mConfig file not found, launching setup wizard...\033[0m\n")
        setupWizard()
    else:
        print("\033[92mConfig file found, continuing...\033[0m\n")
    readConfigFile()

def readConfigFile():
    global configfile
    with open("./config.json", "r") as jsonconfig:
        configfile = json.load(jsonconfig)

def setupWizard():
    input("\033[1mWelcome to the setup wizard!\n"
            "I will guide you through the configuration process. "
            "At the end of it, a config file named \"config.json\" will be created in current directory.\033[0m\n"
            "\033[96mFirst, let's add personal AbuseIPDB API key to the config file, "
            "so that you don't need to type it in manually every time you start the program.\n"
            "To do that, go to \"https://www.abuseipdb.com/\", make an account, or log in if you already have one. "
            "Next, click on your profile name in the top right corner. "
            "There should be a menu, where you can choose between \"Account\" and \"Logout\". Click on \"Account\". "
            "You should have been redirected to your profile page. Click on the \"API\" tab. In the \"Keys\" container "
            "you can see all created API keys. If you already have one (or more) you can just copy it. "
            "If you don't have one yet, click on \"Create Key\" on the right in abovementioned container."
            "You will need to name it and click on \"CREATE\" button to create the key. Once done, you can just copy the key "
            "into the clipboard and continue with the wizard. To do that, just click ENTER on your keyboard. :)\033[0m\n")
    addApiKey()
    while True:
        match input("\033[96mHey, it seems like you have added your first API key, cool!\n"
                    "Now, this program can generate reports for you. Would you like to generate reports at the end"
                    "of each run? Type in \"1\" for yes, or \"0\" for no.\033[0m\n"):
            case "0":
                answerreports = False
                break
            case "1":
                answerreports = True
                while True:
                    match input("\033[96mWhat format would you like your reports in? You can choose between \"CSV\" and \"JSON\"."
                                "Type \"0\" for CSV, or \"1\" for JSON\033[0m\n"):
                        case "0":
                            answerreportsformat = "csv"
                            break
                        case "1":
                            answerreportsformat = "json"
                            break
                        case _:
                            print("\033[91mInvalid value, please choose between \"0\" and \"1\".\033[0m\n")
            case _:
                print("\033[91mInvalid value, please choose between \"0\" and \"1\".\033[0m\n")
    while True:
        print("\033[96Allright, reports done. Let's dive into the actual data. There are 10 values that can be returned "
            "by this program. Before I give you the list of all of them, I need to explain you a few things.\033[0m\n"
            "\033[93mFirstly, these settings are applied to individual runs of the program, as well as to the reports "
            "themselves (if set). Secondly, the value of each field is set to \"True\" as default, so if you just "
            "press \"ENTER\" after asked for an input, you will get all available information. Lastly, you have to "
            "type the number of the fields you want to include. You can choose between 0 and 7, each number must be "
            "separated with a comma symbol \",\". There can be \033[91mNO\033[0m spaces after commas.\033[0m\n"
            "\033[96mipaddress - contains the IP address and will always be included.\n"
            "isWhitelisted - this field will return value \"True\" or \"False\", depending on whitelist status. "
            "To include it type \"0\"\n"
            "abuseConfidence - abuse confidence score, will be explained in the next step. This field will always"
            "be included.\n"
            "countryCode - country code associated with the IP address. To include it type \"1\"\n"
            "usageType - what the IP is used for. To include it type \"2\"\n"
            "isp - ISP associated with the IP address. To include it type \"3\"\n"
            "domain - domain name associated with the IP address. To include it type \"4\"\n"
            "isTor - is the IP address associated with the TOR network. Returns values \"True\" or \"False\"."
            "To include it type \"5\"\n"
            "totalReports - how many user reports are associated with the IP address. To include it type \"6\"\n"
            "lastReport - when was the last report made. To include it type \"7\"\033[0m\n")
        customfieldsuserinput = input()
        customfieldsarray = [int(num) for num in customfieldsuserinput.split(",")]

        if not customfieldsarray:
            customfieldsvalue = False
            break
        else:
            customfieldsvalue = True
            iswhitelistedcustom = False
            countrycode = False
            usagetypecustom = False
            ispcustom = False
            domaincustom = False
            istorcustom = False
            totalreportscustom = False
            lastreportcustom = False
            for field in customfieldsarray:
                match int(field):
                    case 0:
                        iswhitelistedcustom = True
                    case 1:
                        countrycode = True
                    case 2:
                        usagetypecustom = True
                    case 3:
                        ispcustom = True
                    case 4:
                        domaincustom = True
                    case 5:
                        istorcustom = True
                    case 6:
                        totalreportscustom = True
                    case 7:
                        lastreportcustom = True
                    case _:
                        print("\033[91mInvalid value. Skipping...")
            break
    ipadressconst = True
    abuseconfidenceconst = True


    while True:
        print("\033[96mOkay, we arrived at the last step. Don't worry, if you followed all the steps and I did not mess "
            "anything up, it is the last time you see this wizard. :)\n"
            "On \"https://www.abuseipdb.com/\" there is a thing called \"Abuse confidence score\". It is a score "
            "you see when you type some IP address in. It is shown as a bar chart and has a value from 0 to 100%, "
            "where 0 means practically no maliciousness and a 100 means it is pretty bad. You can read more about "
            "that here: \"https://www.abuseipdb.com/faq.html\". I believe that it does not make sense to include "
            "any IP addresses of which Abuse confidence score is 0, so that is the value that is going to be ingored "
            "when you just press \"ENTER\". Cool thing is, you can set the threshold yourself. To do that, just "
            "type the value between 0-100 into the console.\033[0m\n"
            "\033[93mNote, that this setting will be applied to the reports as well as the individual runs of the program, "
            "even when reports are not being generated.\033[0m\n")
        threshold = int(input())
        if threshold >= 0 <= 100:
            #have to test it
            break
    makeNewConfigFile(confidenceThreshold=threshold, isOutputCustom=customfieldsvalue, wantsReports=answerreports, reportFormat=answerreportsformat, isWhitelistedCustom=iswhitelistedcustom, countryCodeCustom=countrycode, usageTypeCustom=usagetypecustom, ispcustom=ispcustom, domainCustom=domaincustom, isTorCustom=istorcustom, totalReportsCustom=totalreportscustom, lastReportCustom=lastreportcustom)

def addApiKey():
    global apikey
    while True:
        match input("What would you like to do now?\n"
                    "Type 1 to add an AbuseIPDB api key and save it to the current directory under \"api.txt\"\n"
                    "Type 2 to provide a path to an AbuseIPDB api key and copy it to the current directory under \"api.txt\"\n"
                    "Type 3 to add an AbuseIPDB api key without saving it (not recommended)\n"
                    "Type 4 to exit\n"):
            case "1":
                apikey = input("Type the api key into the console:\n")
            case "2":
                apikeymanualpathinput = input("Type the path to the api key into the console (without quotes):\n")
                with open(apikeymanualpathinput, "r") as readfile:
                    apikey = str(readfile.read())
                return "1"
            case "3":
                apikey = input("Type the api key into the console:\n")
                return "2"
            case "4":
                exit(1)
            case _:
                print("\033[91mInvalid value, please choose between \"1\", \"2\", \"3\" or \"4\".\033[0m\n")

def makeNewConfigFile(**kwargs):
    apikeysave = kwargs.get("apikeysave")
    confidenceThreshold = kwargs.get("confidenceThreshold")
    isOutputCustom = kwargs.get("isOutputCustom")
    wantsReports = kwargs.get("wantsReports")
    reportFormat = kwargs.get("reportFormat")
    ipaddress = kwargs.get("ipaddress")
    isWhitelisted = kwargs.get("isWhitelistedCustom")
    abuseConfidence = kwargs.get("abuseConfidenceCustom")
    countryCode = kwargs.get("countryCodeCustom")
    usageType = kwargs.get("usageTypeCustom")
    isp = kwargs.get("ispCustom")
    domain = kwargs.get("domainCustom")
    isTor = kwargs.get("isTorCustom")
    totalReports = kwargs.get("totalReportsCustom")
    lastReport = kwargs.get("lastReportCustom")
    with open("./config.json", "w") as jsonconfigfilewrite:
        json.dumps()


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

def generateReportCSV():
    print("Coming soon")

def generateReportJSON():
    print("Coming soon")

if __name__ == '__main__':
    menu()