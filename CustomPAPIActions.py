'''
// I dedicate all this code, all my work, to my wife, who will
// have to support me once it gets released into the public.
Author: Vreddhi Bhat
Contact: vbhat@akamai.com
'''

from papitools.papitools import Papitools
import configparser
import requests, logging, json, sys
from akamai.edgegrid import EdgeGridAuth
import urllib
import json
import argparse
import generateHtml
#Program start here



parser = argparse.ArgumentParser()
parser.add_argument("-act","--activate", help="Activate configuration specified in property_name in .config.txt", action="store_true")
parser.add_argument("-emails","--emails", help="Email ids to be notified")
parser.add_argument("-notes","--notes", help="Email ids to be notified")
parser.add_argument("-copy","--copyConfig", help="Used to copy source configuration to destination configuration", action="store_true")
parser.add_argument("-config","--Configuration", help="Name of Configuration/Property")
parser.add_argument("-version","--Version", help="Version of Configuration/Property")
parser.add_argument("-network","--network", help="Network to be activated on")
parser.add_argument("-src_config","--fromConfiguration", help="Name of fromConfiguration")
parser.add_argument("-dest_config","--toConfiguration", help="Name of toConfiguration")
parser.add_argument("-from_version","--fromVersion", help="Config version of fromConfiguration")
parser.add_argument("-to_version","--toVersion", help="Config version of toConfiguration")
parser.add_argument("-d","--download", help="Download configuration and display JSON in console", action="store_true")
parser.add_argument("-ar","--addredirects", help="Append Redirect Rules from a csv File", action="store_true")
parser.add_argument("-pc","--propertyCount", help="Count properties", action="store_true")
parser.add_argument("-fmp","--ForwardPath", help="Add FMP Rules from a csv File", action="store_true")
parser.add_argument("-clone","--cloneConfig", help="Clone a configuration", action="store_true")
parser.add_argument("-delete","--deleteProperty", help="Delete a configuration", action="store_true")
parser.add_argument("-fetchadvanced","--advancedCheck", help="Check advanced matches", action="store_true")
parser.add_argument("-listproducts","--listproducts", help="List all the products in contract", action="store_true")
parser.add_argument("-cloneConfigList","--cloneConfigList", help="Clone a list of configurations", action="store_true")
parser.add_argument("-cloneAllConfig","--cloneAllConfig", help="Clone all configurations under account", action="store_true")
parser.add_argument("-updateSRTO","--updateSRTO", help="Update the SRTO of sureroute in a configuration", action="store_true")
parser.add_argument("-replaceString","--replaceString", help="Find and replace a string in configuration", action="store_true")
parser.add_argument("-updateRuleSet","--updateRuleSet", help="Update rules set to latest version for all configurations in account", action="store_true")
parser.add_argument("-checkErrors","--checkErrors", help="Check for errors in configurations", action="store_true")
parser.add_argument("-findString","--findString", help="Find a string pattern in configuration", action="store_true")
parser.add_argument("-stringToFind","--stringToFind", help="Find a string pattern in configuration")
parser.add_argument("-activateConfigs","--activateConfigs", help="Activate configurations specified in a list", action="store_true")
parser.add_argument("-removeBehavior","--removeBehavior", help="Activate configurations specified in a list")
parser.add_argument("-createVersion","--createVersion", help="Create a new configurataion version",action="store_true")


#DNS
parser.add_argument("-dnstest", help="Activate configurations specified in a list",action="store_true")


args = parser.parse_args()



try:
    config = configparser.ConfigParser()
    config.read('config_MSIC.txt')
    client_token = config['CREDENTIALS']['client_token']
    client_secret = config['CREDENTIALS']['client_secret']
    access_token = config['CREDENTIALS']['access_token']
    access_hostname = config['CREDENTIALS']['access_hostname']
    session = requests.Session()
    session.auth = EdgeGridAuth(
    			client_token = client_token,
    			client_secret = client_secret,
    			access_token = access_token
                )
    print('Establishing Connection')
except (NameError,AttributeError):
    print("\nUse -h to know the options to run program\n")
    exit()

if not args.copyConfig and not args.download and not args.activate and not args.addredirects and not \
    args.propertyCount and not args.ForwardPath and not args.fromConfiguration and not args.toConfiguration and not \
    args.fromVersion and not args.toVersion and not args.Configuration and not args.Version and not args.network and not\
    args.cloneConfig and not args.deleteProperty and not args.advancedCheck and not args.emails and not args.notes and not\
    args.listproducts and not args.cloneConfigList and not args.cloneAllConfig and not args.updateSRTO and not args.replaceString and not\
    args.updateRuleSet and not args.checkErrors and not args.findString and not args.stringToFind and not args.activateConfigs and not\
    args.removeBehavior and not args.dnstest and not args.createVersion:
    print("\nUse -h to know the options to run program\n")
    exit()


def getRuleNames(parentRule,parentruleName,propertyName,filehandler):
    for eachRule in parentRule:
        ruleName = parentruleName + " --> " + eachRule['name']
        for eachCritera in eachRule['criteria']:
            if eachCritera['name'] == 'matchAdvanced':
                filehandler.writeChildRules('<b>' + 'Rule: ' + ruleName + '</b>')
                filehandler.writeAnotherLine(eachCritera['options']['openXml'][1:-2])
        if len(eachRule['children']) != 0:
            getRuleNames(eachRule['children'],ruleName,propertyName,filehandler)

if args.activate:
    print("\nHang on... while we activate configuration.. This will take time..\n")
    print("\nSetting up the pre-requisites...\n")
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nTrying to activate configuration..\n")
    property_name = args.Configuration
    version = args.Version
    network = args.network
    emails = args.emails
    notes = args.notes
    activationResponseObj = PapiToolsObject.activateConfiguration(session, property_name, version, network, emails, notes)
    print(json.dumps(activationResponseObj.json()))


if args.activateConfigs:
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    #Update the propertyNames or configuration names in below list
    property_names = ["managed-test.bestbuy.com_pm" ,"managed-test-ssl.bestbuy.com" ,"www.stage.bestbuy.com_pm","www-ssl.stage.bestbuy.com_pm"]
    for propertyName in property_names:
        print("\nTrying to activate configuration.. " + propertyName + "\n")
        property_name = propertyName
        versionResponse = PapiToolsObject.getVersion(session, propertyName)
        if versionResponse.status_code != 404:
            versionsList= versionResponse.json()['versions']['items']
            for everyVersion in versionsList:
                version = everyVersion['propertyVersion']
            print('Latest production version of ' + propertyName + ' is ' + str(version))
            print("\nHang on... while we activate the configuration.. " + propertyName + '\n')
            network = 'STAGING'
            emails = 'vbhat@akamai.com'
            notes = 'Activating configuration via script'
            activationResponseObj = PapiToolsObject.activateConfiguration(session, property_name, version, network, emails, notes)
            print(json.dumps(activationResponseObj.json()))
        else:
            print(propertyName + ' version not found')
            print(print(json.dumps(versionResponse.json())))

if args.createVersion:
    print("\nHang on... while we activate configuration.. This will take time..\n")
    print("\nSetting up the pre-requisites...\n")
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nTrying to activate configuration..\n")
    property_name = args.Configuration
    baseVersion = args.Version
    createVersionResponseObj = PapiToolsObject.createVersion(session, baseVersion, property_name)
    print(json.dumps(createVersionResponseObj.json()))

if args.copyConfig:
    #Initialise Source Property Information
    print("\nHang on... while we copy rules.. This will take time..")
    fromVersion = args.fromVersion
    toVersion = args.toVersion
    fromConfiguration = args.fromConfiguration
    toConfiguration = args.toConfiguration
    if fromVersion is None or toVersion is None or fromConfiguration is None or toConfiguration is None:
        print('\nMandatory arguments missing\n')
        exit()
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    fromRulesObject = PapiToolsObject.getPropertyRules(session, fromConfiguration, fromVersion)
    if fromRulesObject.status_code != 200:
        print(fromRulesObject.json())
        exit()
    fromPropertyRules = fromRulesObject.json()['rules']
    #Initialise destination Property Information
    toPropertyDetails = PapiToolsObject.getPropertyRules(session, toConfiguration, toVersion).json()
    toPropertyDetails['rules'] = fromPropertyRules
    PapiToolsObject.uploadRules(session, toPropertyDetails, toConfiguration, toVersion)

if args.download:
    print("\nSetting up the pre-requisites...\n")
    property_name = args.Configuration
    version = args.Version
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nHang on... while we download the json data.. ")
    print("\nHang on... We are almost set, fetching the rules now.. This will take time..\n")
    rulesObject = PapiToolsObject.getPropertyRules(session,property_name,version)
    print(json.dumps(rulesObject.json()))

if args.addredirects:
    csvTojsonObj = csvTojsonParser.optionSelector()
    print("\nConvert csv to Json is finished.. ")
    print("\nSetting up the pre-requisites...\n")
    redirectJsonData = csvTojsonObj.parseCSVFile()
    destPropertyObject = PropertyDetails.Property(dest_access_hostname, dest_property_name, dest_version, dest_notes, dest_emails)
    PAPIWrapperObject = PAPIWrapper.PAPIWrapper()
    print("\nWe are now fetching the property details like ID, contractId and GroupID\n")
    destGroupsInfo = PAPIWrapperObject.getGroups(destSession, destPropertyObject)
    PAPIWrapperObject.getPropertyInfo(destSession, destPropertyObject, destGroupsInfo)
    print("\nHang on... Fetching property rules now.. This will take time..\n")
    destPropertyRules = PAPIWrapperObject.getPropertyRules(destSession, destPropertyObject).json()
    destPropertyRules['rules']['children'].append(redirectJsonData)
    print("\nHang on... We are almost set, Updating with the rules now.. This will again take time..\n")
    updateObjectResponse = PAPIWrapperObject.uploadRules(destSession, destPropertyObject, destPropertyRules)

if args.ForwardPath:
    csvTojsonObj = csvTojsonParser.optionSelector()
    print("\nConvert csv to Json is finished.. ")
    print("\nSetting up the pre-requisites...\n")
    FMPJsonData = csvTojsonObj.parseCSVFile()
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nHang on... while we download the json data.. ")
    print("\nHang on... We are almost set, fetching the rules now.. This will take time..\n")
    propertyRules = PapiToolsObject.getPropertyRules(session,property_name,version).json()
    print(json.dumps(propertyRules))
    propertyRules['rules']['children'].append(FMPJsonData)
    print("\nHang on... We are almost set, Updating with the rules now.. This will again take time..\n")
    updateObjectResponse = PapiToolsObject.uploadRules(session, propertyRules,property_name, version)
    print(updateObjectResponse.json())


if args.propertyCount:
    print("\nHang on... while we Count properties.. ")
    propertyObject = PropertyDetails.Property(access_hostname, property_name, version, notes, emails)
    print("\nSetting up the pre-requisites...\n")
    PAPIWrapperObject = PAPIWrapper.PAPIWrapper()
    groupsInfo = PAPIWrapperObject.getGroups(session, propertyObject)
    print("\nWe are now fetching the property details like ID, contractId and GroupID\n")
    count = 1
    for eachDataGroup in groupsInfo.json()['groups']['items']:
        try:
            contractId = [eachDataGroup['contractIds'][0]]
            groupId = [eachDataGroup['groupId']]
            url = 'https://' + propertyObject.access_hostname + '/papi/v0/properties/?contractId=' + contractId[0] +'&groupId=' + groupId[0]
            propertiesResponse = session.get(url)
            if propertiesResponse.status_code == 200:
                propertiesResponseJson = propertiesResponse.json()
                propertiesList = propertiesResponseJson['properties']['items']
                for propertyInfo in propertiesList:
                    propertyName = propertyInfo['propertyName']
                    propertyId = propertyInfo['propertyId']
                    propertyContractId = propertyInfo['contractId']
                    propertyGroupId = propertyInfo['groupId']
                    print(str(count) + ". propertyName: " + propertyName)
                    count += 1
        except KeyError:
            pass

if args.cloneConfig:
    property_name = args.fromConfiguration
    new_property_name = args.toConfiguration
    version = args.fromVersion
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nHang on... while we clone configuration.. ")
    cloneResponse = PapiToolsObject.cloneConfig(session, property_name,new_property_name,version)
    if cloneResponse.status_code == 200:
        print('SUCCESS: ' + cloneResponse.json()['propertyLink'])
    else:
        print('FAILURE: ' + str(cloneResponse.json()))

if args.deleteProperty:
    property_name = args.Configuration
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nHang on... while we delete configuration.. ")
    deleteResponse = PapiToolsObject.deleteProperty(session, property_name)
    if deleteResponse.status_code == 200:
        print('SUCCESS: ' + str(deleteResponse.json()))
    else:
        print('FAILURE: ' + str(deleteResponse.json()))

if args.listproducts:
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    PapiToolsObject.listProducts(session)

if args.advancedCheck:
    papiToolsObject = Papitools(access_hostname=access_hostname)
    groupResponse = papiToolsObject.getGroups(session)
    output_file_name = "advancedMdtCheck.html"
    filehandler = generateHtml.htmlWriter(output_file_name)
    filehandler.writeData(filehandler.start_data)
    filehandler.writeData(filehandler.div_start_data)
    propertyNameList = []
    PropertyNumber = 1
    for everyGroup in groupResponse.json()['groups']['items']:
        try:
            groupId = everyGroup['groupId']
            contractId = everyGroup['contractIds'][0]
            properties = papiToolsObject.getAllProperties(session, contractId, groupId)
            for everyPropertyGroup in properties.json()['properties']['items']:
                if everyPropertyGroup['propertyId'] not in propertyNameList:
                    propertyName = everyPropertyGroup['propertyName']
                    filehandler.writeData(filehandler.table_start_data)
                    filehandler.writeTableHeader(str(PropertyNumber) + '. '+ propertyName)
                    PropertyNumber += 1
                    propertyNameList.append(everyPropertyGroup['propertyId'])
                    print('Property: ' + propertyName + ' Under process\n')
                    rulesUrlResponse = papiToolsObject.getPropertyRulesfromPropertyId(session, everyPropertyGroup['propertyId'], everyPropertyGroup['latestVersion'], everyPropertyGroup['contractId'], everyPropertyGroup['groupId'])
                    rulesUrlJsonResponse = rulesUrlResponse.json()
                    try:
                        RulesList = rulesUrlJsonResponse['rules']['children']
                        for eachRule in RulesList:
                            for eachCritera in eachRule['criteria']:
                                if eachCritera['name'] == 'matchAdvanced':
                                    filehandler.writeChildRules('<b>' + 'Rule: ' + eachRule['name'] + '</b>' )
                                    filehandler.writeAnotherLine(eachCritera['options']['openXml'][1:-2])
                            if len(eachRule['children']) != 0:
                                ruleName = eachRule['name']
                                getRuleNames(eachRule['children'],ruleName,propertyName,filehandler)
                    except KeyError:
                        print("Looks like there are no rules other than default rule")
        except KeyError:
            print('Looks like No contract or group ID was fetched in one of the group Response')
    filehandler.writeData(filehandler.div_start_data)


if args.cloneConfigList:
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    #Update the propertyNames or configuration names in below list
    property_names = ['www-msci-uat','msci-support-cdn']
    for propertyName in property_names:
        new_property_name = propertyName + '_ionStd'
        print('Hold on.. While we fetch the latest production version for ' + propertyName + '\n')
        versionResponse = PapiToolsObject.getVersion(session, propertyName, activeOn="PRODUCTION")
        if versionResponse.status_code != 404:
            versionsList= versionResponse.json()['versions']['items']
            for everyVersion in versionsList:
                version = everyVersion['propertyVersion']
            print('Latest production version of ' + propertyName + ' is ' + str(version))
            print("\nHang on... while we clone configuration.. " + propertyName + '\n')
            cloneResponse = PapiToolsObject.cloneConfig(session, propertyName,new_property_name,version)
            if cloneResponse.status_code == 201:
                print('SUCCESS: ' + new_property_name + 'is created. Here is the link to it' + cloneResponse.json()['propertyLink'] + '\n')
            else:
                print('FAILURE: ' + str(cloneResponse.json()))
        else:
            print(propertyName + ' was not cloned because it is not active in PRODUCTION. Try manually or report to developer')

if args.cloneAllConfig:
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    groupResponse = PapiToolsObject.getGroups(session)
    propertyNameList = [] #List to determine duplication of property names
    PropertyNumber = 1
    print('Fetching all properties\n')
    for everyGroup in groupResponse.json()['groups']['items']:
        try:
            groupId = everyGroup['groupId']
            contractId = everyGroup['contractIds'][0]
            properties = PapiToolsObject.getAllProperties(session, contractId, groupId)
            for everyPropertyGroup in properties.json()['properties']['items']:
                if everyPropertyGroup['propertyName'] not in propertyNameList:
                    propertyName = everyPropertyGroup['propertyName']
                    PropertyNumber += 1
                    propertyNameList.append(propertyName)
                    print('Property: ' + propertyName + ' added to list of properties')
        except KeyError:
            print('Looks like No contract or group ID was fetched in one of the group Response')
    #Below logic clones the configurations based on list populated above
    for propertyName in propertyNameList:
        new_property_name = propertyName + '_ionStd'
        print('Hold on.. While we fetch the latest production version for ' + propertyName + '\n')
        versionResponse = PapiToolsObject.getVersion(session, propertyName, activeOn="PRODUCTION")
        if versionResponse.status_code != 404:
            versionsList= versionResponse.json()['versions']['items']
            for everyVersion in versionsList:
                version = everyVersion['propertyVersion']
            print('Latest production version of ' + propertyName + ' is ' + str(version))
            print("\nHang on... while we clone configuration.. " + propertyName + '\n')
            cloneResponse = PapiToolsObject.cloneConfig(session, propertyName,new_property_name,version)
            if cloneResponse.status_code == 201:
                print('SUCCESS: ' + new_property_name + 'is created. Here is the link to it' + cloneResponse.json()['propertyLink'] + '\n')
            else:
                print('FAILURE: ' + str(cloneResponse.json()))
        else:
            print(propertyName + ' was not cloned because it is not active in PRODUCTION. Try manually or report to developer')

if args.updateSRTO:
    property_name = args.Configuration
    version = args.Version
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nHang on... while we download the json data.. ")
    print("\nHang on... We are almost set, fetching the rules now.. This will take time..\n")
    propertyJson = PapiToolsObject.getPropertyRules(session,property_name,version).json()
    #print(json.dumps(propertyJson))
    for everyChileRule in  propertyJson['rules']['children']:
        if everyChileRule['name'] == 'Performance':
            for everyBehavior in everyChileRule['behaviors']:
                if everyBehavior['name'] == 'sureRoute':
                    print(everyBehavior['options']['testObjectUrl'])
                    everyBehavior['options']['testObjectUrl'] = '/changed/again/by/papi.html'
    print("\nHang on... We are almost set, Updating with the rules now.. This will again take time..\n")
    updateObjectResponse = PapiToolsObject.uploadRules(session, propertyJson,property_name, version)
    print(updateObjectResponse.json())
    print("\nLooks like it is done\n")

if args.replaceString:
    print("\nSetting up the pre-requisites...\n")
    property_name = args.Configuration
    version = args.Version
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nHang on... while we download the json data.. ")
    print("\nHang on... We are almost set, fetching the rules now.. This will take time..\n")
    propertyJson = PapiToolsObject.getPropertyRules(session,property_name,version).json()
    updatedpropertyJson = json.loads(json.dumps(propertyJson).replace("browse-east.cloud-test.bestbuy.com.akadns.net", "web-east.test.browse.bestbuy.com"))
    updateObjectResponse = PapiToolsObject.uploadRules(session, updatedpropertyJson,property_name, version)
    print(json.dumps(updateObjectResponse.json()))
    print("\nLooks like it is done\n")

if args.updateRuleSet:
    print("\nSetting up the pre-requisites...\n")
    property_name = args.Configuration
    version = args.Version
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nHang on... while we download the json data.. ")
    print("\nHang on... We are almost set, fetching the rules now.. This will take time..\n")
    ruleFormatResponse = PapiToolsObject.listRuleFormats(session)
    latestTimeStamp = ''
    for everyItem in ruleFormatResponse.json()['ruleFormats']['items']:
        if everyItem[1:5] == '2016':
            latestTimeStamp = everyItem
    ruleTreeResponse = PapiToolsObject.getRuleTree(session, property_name, version,latestTimeStamp)
    print(json.dumps(ruleTreeResponse.json()))
    print("Successfully retrieved the rules Tree, we now need to try upgrading it to latest version")
    updateruleTreeResponse = PapiToolsObject.updateRuleTree(session, property_name, version, latestTimeStamp)
    print(str(updateruleTreeResponse.status_code))
    print(json.dumps(updateruleTreeResponse.json()))

if args.checkErrors:
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    groupResponse = PapiToolsObject.getGroups(session)
    propertyNameList = [] #List to determine duplication of property names
    PropertyNumber = 1
    ruleFormatResponse = PapiToolsObject.listRuleFormats(session)
    latestTimeStamp = ''
    for everyItem in ruleFormatResponse.json()['ruleFormats']['items']:
        if everyItem[1:5] == '2016':
            latestTimeStamp = everyItem
    print('Fetching all properties\n')
    for everyGroup in groupResponse.json()['groups']['items']:
        try:
            groupId = everyGroup['groupId']
            contractId = everyGroup['contractIds'][0]
            properties = PapiToolsObject.getAllProperties(session, contractId, groupId)
            for everyPropertyGroup in properties.json()['properties']['items']:
                if everyPropertyGroup['propertyName'] not in propertyNameList:
                    propertyName = everyPropertyGroup['propertyName']
                    PropertyNumber += 1
                    if propertyName.endswith('_ionStd'):
                        propertyNameList.append(propertyName)
                        print('Property: ' + propertyName + ' added to list of properties')
        except KeyError:
            print('Looks like No contract or group ID was fetched in one of the group Response')
    #Below logic clones the configurations based on list populated above
    for propertyName in propertyNameList:
        ruleTreeResponse = PapiToolsObject.getRuleTree(session, propertyName,'1',latestTimeStamp)
        if 'errors'in ruleTreeResponse.json():
            print('Error Configuration: ' + propertyName )

if args.findString:
    papiToolsObject = Papitools(access_hostname=access_hostname)
    groupResponse = papiToolsObject.getGroups(session)
    output_file_name = "behaviorStringCheck.html"
    filehandler = generateHtml.htmlWriter(output_file_name)
    filehandler.writeData(filehandler.start_data)
    filehandler.writeData(filehandler.div_start_data)
    propertyIdList = []
    PropertyNumber = 1
    for everyGroup in groupResponse.json()['groups']['items']:
        try:
            groupId = everyGroup['groupId']
            for contractId in everyGroup['contractIds']:
                properties = papiToolsObject.getAllProperties(session, contractId, groupId)
                for everyPropertyGroup in properties.json()['properties']['items']:
                    if everyPropertyGroup['propertyId'] not in propertyIdList:
                        propertyName = everyPropertyGroup['propertyName']
                        propertyIdList.append(everyPropertyGroup['propertyId'])
                        print(str(PropertyNumber) + '. Property: ' + propertyName + ' Under process\n')
                        rulesUrlResponse = papiToolsObject.getPropertyRulesfromPropertyId(session, everyPropertyGroup['propertyId'], everyPropertyGroup['latestVersion'], everyPropertyGroup['contractId'], everyPropertyGroup['groupId'])
                        propertyRulesText = json.dumps(rulesUrlResponse.json())
                        if args.stringToFind in propertyRulesText and 'application/json*' not in propertyRulesText:
                            filehandler.writeData(filehandler.table_start_data)
                            filehandler.writeTableHeader(str(PropertyNumber) + '. '+ propertyName)
                            filehandler.writeAnotherLine(args.stringToFind + ' is Found')
                            PropertyNumber += 1
                        else:
                            pass
        except KeyError:
            print('Looks like No contract or group ID was fetched in one of the group Response')
    filehandler.writeData(filehandler.div_end_data)


if args.removeBehavior:
    behaviorName = args.removeBehavior
    print("\nSetting up the pre-requisites...\n")
    property_name = args.Configuration
    version = args.Version
    PapiToolsObject = Papitools(access_hostname=access_hostname)
    print("\nHang on... while we download the json data.. ")
    print("\nHang on... We are almost set, fetching the rules now.. This will take time..\n")
    propertyJson = PapiToolsObject.getPropertyRules(session,property_name,version).json()
    new_Behaviorlist = [behavior for behavior in propertyJson['rules']['behaviors'] if behavior['name'] != behaviorName]
    propertyJson['rules']['behaviors'] = new_Behaviorlist #Assign it Back to same object in memory
    updateObjectResponse = PapiToolsObject.uploadRules(session, propertyJson,property_name, version)
    print("\nLooks like it is done\n")


if args.dnstest:
    dnsUrl = 'https://' + access_hostname + '/data-dns/v1/traffic/vistaprint.com?start=20170417&start_time=16:00&end=20170417&end_time=16:30'
    response = session.get(dnsUrl)
    print(response.text)

#print('\n**********DONE**********')
