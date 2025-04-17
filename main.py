import csv
import json
import os.path
import requests
import re


global apikey
global apikeytemp
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
    global apikey
    global configfile
    apikey = configfile['config']['apiKey']
    if apikey != "":
        apikey = apikey
    else:
        apikey = apikeytemp
    while True:
        match (input("Hello there, hope you are having a great day!\n"
                "What would you like to do?\n"
                "Type a number corresponding to the option you want to choose:\n\n"
                "1. Check single, or multiple (separated by a comma, without spaces) IPs against AbuseIPDB\n"
                "2. Provide a CSV file containing IP addresses and check against AbuseIPDB\n"
                "9. Settings\n"
                "0. Exit\n")):
            case "1":
                iparr = input("Please type the IP addresses, separated by a comma, without spaces.\n")
                inputuser = [ip for ip in iparr.split(",")]
                processIPsAbuseDB(processIPArray(inputuser), apikey)
            case "2":
                processIPsAbuseDB(processIPArray(processCSV()), apikey)
            case "3":
                print("Feature not implemented yet.")
            case "9":
                print("Feature not implemented yet.")
            case "0":
                exit("Exitting...")
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
            "If you don't have one yet, click on \"Create Key\" on the right in abovementioned container. "
            "You will need to name it and click on \"CREATE\" button to create the key. Once done, you can just copy the key "
            "into the clipboard and continue with the wizard. To do that, just click ENTER on your keyboard. :)\033[0m\n")
    addApiKey()
    while True:
        answerreports = False
        answerreportsformat = False
        match input("\033[96mHey, it seems like you have added your first API key, cool!\n"
                    "Now, this program can generate reports for you. Would you like to generate reports at the end "
                    "of each run? Type in \"1\" for yes, or \"0\" for no.\033[0m\n"):
            case "0":
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
                break
            case _:
                print("\033[91mInvalid value, please choose between \"0\" and \"1\".\033[0m\n")
    while True:
        print("\033[96mAllright, reports done. Let's dive into the actual data. There are 10 values that can be returned "
            "by this program. Before I give you the list of all of them, I need to explain you a few things.\033[0m\n"
            "\033[93mFirstly, these settings are applied to individual runs of the program, as well as to the reports "
            "themselves (if set). Secondly, the value of each field is set to \"True\" as default, so if you just "
            "press \"ENTER\" after asked for an input, you will get all available information. Lastly, you have to "
            "type the number of the fields you want to include. You can choose between 0 and 7, each number must be "
            "separated with a comma symbol \",\". There can be \033[91mNO \033[93mspaces after commas.\033[0m\n"
            "\033[96mipaddress - contains the IP address and will always be included.\n"
            "isWhitelisted - this field will return value \"True\" or \"False\", depending on whitelist status. "
            "To include it type \"0\"\n"
            "abuseConfidence - abuse confidence score, will be explained in the next step. This field will always "
            "be included.\n"
            "countryCode - country code associated with the IP address. To include it type \"1\"\n"
            "usageType - what the IP is used for. To include it type \"2\"\n"
            "isp - ISP associated with the IP address. To include it type \"3\"\n"
            "domain - domain name associated with the IP address. To include it type \"4\"\n"
            "isTor - is the IP address associated with the TOR network. Returns values \"True\" or \"False\"."
            "To include it type \"5\"\n"
            "totalReports - how many user reports are associated with the IP address. To include it type \"6\"\n"
            "lastReport - when was the last report made. To include it type \"7\"\033[0m\n")

        iswhitelistedcustom = False
        countrycode = False
        usagetypecustom = False
        ispcustom = False
        domaincustom = False
        istorcustom = False
        totalreportscustom = False
        lastreportcustom = False
        customfieldsuserinput = input()
        customfieldsarray = [choice for choice in customfieldsuserinput.split(",")]

        if customfieldsarray[0] == "":
            customfieldsvalue = False
            break
        else:
            customfieldsvalue = True
            for field in customfieldsarray:
                match field:
                    case "0":
                        iswhitelistedcustom = True
                        print("\033[92mValue of isWhitelisted set to True.\033[0m")
                    case "1":
                        countrycode = True
                        print("\033[92mValue of countryCode set to True.\033[0m")
                    case "2":
                        usagetypecustom = True
                        print("\033[92mValue of usageType set to True.\033[0m")
                    case "3":
                        ispcustom = True
                        print("\033[92mValue of isp set to True.\033[0m")
                    case "4":
                        domaincustom = True
                        print("\033[92mValue of domain set to True.\033[0m")
                    case "5":
                        istorcustom = True
                        print("\033[92mValue of isTor set to True.\033[0m")
                    case "6":
                        totalreportscustom = True
                        print("\033[92mValue of totalReports set to True.\033[0m")
                    case "7":
                        lastreportcustom = True
                        print("\033[92mValue of lastReport set to True.\033[0m")
                    case _:
                        print("\033[91mInvalid value. Skipping...\033[0m")
            break

    while True:
        print("\033[96mOkay, we arrived at the last step. Don't worry, if you followed all the steps and I did not mess "
            "anything up, it is the last time you see this wizard. :)\n"
            "On \"https://www.abuseipdb.com/\" there is a thing called \"Abuse confidence score\". It is a score "
            "you see when you type some IP address in. It is shown as a bar chart and has a value from 0 to 100%, "
            "where 0 means practically no maliciousness and a 100 means it is pretty bad. You can read more about "
            "that here: \"https://www.abuseipdb.com/faq.html\". I believe that it does not make sense to include "
            "any IP addresses of which Abuse confidence score is 0, so that is the value that is going to be ingored "
            "when you just press \"ENTER\". Cool thing is, you can set the threshold yourself. To do that, just "
            "type the value between 0-100 into the console and press \"ENTER\".\033[0m\n"
            "\033[93mNote, that this setting will be applied to the reports as well as the individual runs of the program, "
            "even when reports are not being generated.\033[0m")
        threshold = int(input())
        if threshold >= 0 <= 100:
            break
        else:
            print("\033[93mDefault value of \"1\" will be set.\033[0m")
            threshold = 1
            break

    if customfieldsvalue:
        makeNewConfigFile(confidencethreshold=threshold, isoutputcustom=customfieldsvalue, wantsreports=answerreports, reportformat=answerreportsformat, iswhitelistedcustom=iswhitelistedcustom, countrycodecustom=countrycode, usagetypecustom=usagetypecustom, ispcustom=ispcustom, domaincustom=domaincustom, istorcustom=istorcustom, totalreportscustom=totalreportscustom, lastreportcustom=lastreportcustom)
        print("\033[92mConfig with custom values added. You can find it in the current directory under \"config.json\".\033[0m")
    else:
        makeNewConfigFile(confidencethreshold=threshold, isoutputcustom=customfieldsvalue, wantsreports=answerreports, reportformat=answerreportsformat)
        print("\033[93mConfig added, custom values will be skipped. You can find it in the current directory under \"config.json\".\033[0m")
    print("\033[96mIt seems like we are done here. Enjoy using the program now!\033[0m")
    menu()

def addApiKey():
    global apikey
    global apikeytemp
    apikey = ""
    apikeytemp = ""

    while True:
        match input("What would you like to do now?\n"
                    "Type 1 to add an AbuseIPDB API key and save it to the current to the config file \"config.json\".\n"
                    "Type 2 to provide a path to an AbuseIPDB API key and copy it to the config file \"config.json\".\n"
                    "Type 3 to add an AbuseIPDB API key without saving it (not recommended)\n"
                    "Type 4 to exit\n"):
            case "1":
                apikey = input("Type the api key into the console:\n")
                break
            case "2":
                apikeymanualpathinput = input("Type the path to the api key into the console (without quotes):\n")
                with open(apikeymanualpathinput, "r") as readfile:
                    apikey = str(readfile.read())
                break
            case "3":
                apikeytemp = input("Type the api key into the console:\n")
                break
            case "4":
                exit(1)
            case _:
                print("\033[91mInvalid value, please choose between \"1\", \"2\", \"3\" or \"4\".\033[0m\n")

def makeNewConfigFile(**kwargs):
    global apikey
    confidencethreshold = kwargs.get("confidencethreshold")
    isoutputcustom = kwargs.get("isoutputcustom")
    wantsreports = kwargs.get("wantsreports")
    reportformat = kwargs.get("reportformat")
    iswhitelisted = kwargs.get("iswhitelistedcustom")
    countrycode = kwargs.get("countrycodecustom")
    usagetype = kwargs.get("usagetypecustom")
    isp = kwargs.get("ispcustom")
    domain = kwargs.get("domaincustom")
    istor = kwargs.get("istorcustom")
    totalreports = kwargs.get("totalreportscustom")
    lastreport = kwargs.get("lastreportcustom")
    configfiledicttosave = {
        "config": {
            "apiKey": apikey,
            "confidenceThreshold": confidencethreshold,
            "isOutputCustom": isoutputcustom,
            "wantsReports": wantsreports,
            "reportFormat": reportformat
        },
        "defaultOutput": {
            "isWhitelisted": True,
            "countryCode": True,
            "usageType": True,
            "isp": True,
            "domain": True,
            "isTor": True,
            "totalReports": True,
            "lastReport": True
        },
        "customOutput": {
            "isWhitelisted": iswhitelisted,
            "countryCode": countrycode,
            "usageType": usagetype,
            "isp": isp,
            "domain": domain,
            "isTor": istor,
            "totalReports": totalreports,
            "lastReport": lastreport
        }
    }
    with open("./config.json", "w") as jsonconfigfilewrite:
        json.dump(configfiledicttosave, jsonconfigfilewrite)

def processCSV():
    csvpath = input("Please provide the path to the CSV file: ")
    csvarr = []
    with open(csvpath, newline="") as csvfile:
        ipreader = csv.reader(csvfile, delimiter=",")
        ipreader.__next__()
        for row in ipreader:
            csvarr.append(row[0])
            csvarr.append(row[1])
    return csvarr

def processIPArray(iparrinput):
    # Use list comprehension to filter out private IPs
    filtered_ips = [ip for ip in iparrinput if not re.search("(10.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|192\\.168\\.[0-9]{1,3}\\.[0-9]{1,3}|172\\.(1[6-9]|2[0-9]|3[0-2])\\.[0-9]{1,3}\\.[0-9]{1,3}|127\\.0\\.0\\.1|0\\.0\\.0\\.0|169\\.254\\.[0-9]{1,3}\\.[0-9]{1,3}|8\\.8\\.8\\.8|8\\.8\\.4\\.4|1\\.1\\.1\\.1)", ip)]
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
    outputDataAbuseIPDB(resultsabuseip)

def outputDataAbuseIPDB(iparr):
    global configfile
    confidencethresholdconfigval = configfile['config']['confidenceThreshold']
    isoutputcustomconfigval = configfile['config']['isOutputCustom']
    if isoutputcustomconfigval == 1:
        readfromdefaultorcustom = 'customOutput'
    else:
        readfromdefaultorcustom = 'defaultOutput'
    outputbooleanvalueslist = [configfile[readfromdefaultorcustom]['isWhitelisted'],
    configfile[readfromdefaultorcustom]['countryCode'],
    configfile[readfromdefaultorcustom]['usageType'],
    configfile[readfromdefaultorcustom]['isp'],
    configfile[readfromdefaultorcustom]['domain'],
    configfile[readfromdefaultorcustom]['isTor'],
    configfile[readfromdefaultorcustom]['totalReports'],
    configfile[readfromdefaultorcustom]['lastReport']]
    for ip in iparr:
        if ip.abuseconfidence >= confidencethresholdconfigval:
            print("IP address: " + ip.ip)
            print(" Abuse confidence: " + str(ip.abuseconfidence))
            for i in range(len(outputbooleanvalueslist)):
                match outputbooleanvalueslist[i]:
                    case True:
                        match i:
                            case 0:
                                print(" Is whitelisted: " + str(ip.whiteliststatus))
                                i += 1
                            case 1:
                                print(" Contry code: " + str(ip.country))
                                i += 1
                            case 2:
                                print(" Usage type: " + str(ip.usagetype))
                                i += 1
                            case 3:
                                print(" ISP (Internet Service Provider): " + str(ip.isp))
                                i += 1
                            case 4:
                                print(" Domain: " + str(ip.domain))
                                i += 1
                            case 5:
                                print(" Is TOR: " + str(ip.istor))
                                i += 1
                            case 6:
                                print(" Total reports: " + str(ip.totalreports))
                                i += 1
                            case 7:
                                print(" Last report at: " + str(ip.lastreportdate))
                                i += 1
                    case _:
                        i += 1
            print("")
        else:
            print("Confidence threshold value of " + str(confidencethresholdconfigval) + " not met for IP: " + str(ip.ip))
    whatReportToGenerate()

    print("\033[91mEverything is done, reports have not been generated, since this feature is not implemented yet.\033[0m\n"
          "Thanks for using the program. If you encountered any problems, please report them under \"Issues\" on the GitHub page of the project. You will be redirected to the menu now.")

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

def whatReportToGenerate():
    global configfile
    wantsreportsconfigval = configfile['config']['wantsReports']
    if wantsreportsconfigval:
        reportformatconfigval = configfile['config']['reportFormat']
        if reportformatconfigval == "csv":
            generateReportCSV()
        elif reportformatconfigval == "json":
            generateReportJSON()
    else:
        print("\033[96mReports are not going to be generated since this option has not been chosen in the setup.\033[0m")

def generateReportCSV():
    print("Coming soon")

def generateReportJSON():
    print("Coming soon")

if __name__ == '__main__':
    menu()