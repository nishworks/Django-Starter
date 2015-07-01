import operator
from ios import Ios
from utils import *
from android import AndroidSheet,androidNS
import json



class AndroidStat():

    def __init__(self, androidsheet):

        self.sheet = androidsheet
        self.nameManufacturerMap = dict()
        self.globalInfo = []
        self.setupGlobalData()

   

    def xStats(self,xOSversion,global_threshold,threshold, roundBy, osmax,osmin):

        result = []
        os_version_list = []
        if xOSversion == 'x':
            os_version_list = self.sheet.xlist
        elif xOSversion == 'xx':
            os_version_list = self.sheet.xxlist
        elif xOSversion == 'xxx':
            os_version_list = self.sheet.xxxlist
        else:
            os_version_list.append(xOSversion)
        print os_version_list

        deviceGroup = []
        osmax = int(osmax)
        osmin = int(osmin)
        os_others = 0.0
        os_results = dict()
        os_global_share = dict()
        for os_version in os_version_list:
            x, xx, xxx = processOsVersion(os_version)
            if xOSversion == 'xx':
                if xx is None:
                    continue
            if xOSversion == 'xxx':
                if xxx is None:
                    continue
            if (int(x) > osmax) or (int(x) < osmin):
                continue
            device_result = self.getDeviceStats(x,xx,xxx,threshold, roundBy)
            processed_os_version = "{0}.{1}.{2}".format(x , xx if xx else "x" , xxx if xxx else "x")
            if device_result[0]['Global share of os'] < global_threshold:
                print "Skipped %s" % processed_os_version
                os_others += device_result[0]['Global share of os']
                continue
            os_results[processed_os_version] = device_result
            os_global_share[processed_os_version] = device_result[0]['Global share of os']
            #deviceGroup.append({"name": processed_os_version, "value" : device_result})
      

        sorted_os_results = sorted(os_global_share.items(), key=operator.itemgetter(1), reverse=True)
        for osresult in sorted_os_results:
            deviceGroup.append({osresult[0] : os_results[osresult[0]]})
        deviceGroup.append({"Global share of other OS in %s"%xOSversion : os_others})
        #deviceGroup.append({"Global share of other OS in %s"%xOSversion : os_others})

        result.append({"name" : "Device Stats - Query", "value" : deviceGroup})
        result.append({"name" : "Global Info", "value" : self.globalInfo})

        return {"Result":result}

 

    def getDeviceStats(self, x, xx, xxx,threshold, roundBy):

        # device:value
        deviceResultSet = dict()
        deviceResultSetPercent = dict()
        manufacturerResultSet = dict()
        manufacturerResultSetPercent = dict()
        
        # Populate dictionaries with matching devices for this OS value
        for record in self.sheet.deviceRecords:

            if record.query_osVersion(x,xx,xxx):
                if record.name not in deviceResultSet:
                    deviceResultSet[record.name] = 0.0
                    self.nameManufacturerMap[record.name] = record.manufacturer
                if record.manufacturer not in manufacturerResultSet:
                    manufacturerResultSet[record.manufacturer] = 0.0
                deviceResultSet[record.name] += record.num_of_views
                manufacturerResultSet[record.manufacturer] += record.num_of_views

        #Calculate sum
        deviceViewsSum = 0.0
        manufacturerViewsSum = 0.0
        for value in deviceResultSet.values():
            deviceViewsSum += value
        for value in manufacturerResultSet.values():
            manufacturerViewsSum += value

        # Populate % values for this OS version
        for key,value in deviceResultSet.iteritems():
            deviceResultSetPercent[key] = round((value/deviceViewsSum)*100,roundBy)
        for key,value in manufacturerResultSet.iteritems():
            manufacturerResultSetPercent[key] = round((value/manufacturerViewsSum)*100,roundBy)


        sorted_impressions = sorted(deviceResultSet.items(), key=operator.itemgetter(1), reverse=True)
        device_impressions = {}
        for tup in sorted_impressions:
            device_impressions[tup[0]] = tup[1]
        sorted_devices = sorted(deviceResultSetPercent.items(), key=operator.itemgetter(1), reverse=True)
        sorted_manufacturers = sorted(manufacturerResultSetPercent.items(), key=operator.itemgetter(1), reverse=True)


        others = 0.0
        total = 0.0
        #JSON for devices
        sorted_device_share = []
        for device in sorted_devices:
            total += device[1]
            if device[1] > threshold:
                #print device
                #print self.nameManufacturerMap[device[0]].upper() + " " + device[0] + " "+ str(device[1])
                #device_share[self.nameManufacturerMap[device[0]].upper() + " " + device[0]] = str(device[1])
                dev_list = []
                dev_list.append({"name" : self.nameManufacturerMap[device[0]].upper() + " " + device[0]})
                dev_list.append({"GlobalShare" : round((device_impressions[device[0]]/self.sheet.total_views)*100,roundBy)})
                dev_list.append({"value" : device[1]})
                dev_list.append({"impressions" : device_impressions[device[0]]})
                

                sorted_device_share.append({"Device": dev_list})
            else:
                others += device[1]
        dev_list = []
        dev_list.append({"name" : "others"})
        dev_list.append({"GlobalShare" : round((long(others*deviceViewsSum)/self.sheet.total_views)*100,roundBy)})
        dev_list.append({"value" : round(others, 4)})
        dev_list.append({"impressions" : long(others*deviceViewsSum)})
        
        sorted_device_share.append({"Device": dev_list})
        

        #JSON for manufacturer
        sorted_manufacturer_share = []
        mothers = 0.0
        for manufacturer in sorted_manufacturers:
            if manufacturer[1] > threshold:
                #print device
                #print self.nameManufacturerMap[device[0]].upper() + " " + device[0] + " "+ str(device[1])
                #manufacturer_share[manufacturer[0]] = str(manufacturer[1])
                sorted_manufacturer_share.append({"manufacturer" : manufacturer[0].upper(), "value" : manufacturer[1]})
            else:
                mothers += manufacturer[1]
        sorted_manufacturer_share.append({"manufacturer" : "Others" , "value" : round(mothers,roundBy)})

        # Final result
        result = []
        result.append({"Global share of os" : round((deviceViewsSum/self.sheet.total_views)*100,roundBy)})
        result.append({"name":"DeviceStats", "value": sorted_device_share})
        result.append({"name":"ManufacturerStats", "value": sorted_manufacturer_share})
        result.append({"name":"Device-stats for Android OS version" ,"value" : "{0}.{1}.{2}".format(x , xx if xx else "x" , xxx if xxx else "x")})
        result.append({"name":"Threshold value", "value":threshold})
        result.append({"name":"Error in approximation", "value" : round(100-total,roundBy)})
        
        return result

    def setupGlobalData(self,threshold=0.8):
        for record in self.sheet.deviceRecords:
            self.nameManufacturerMap[record.name] = record.manufacturer

        globalDeviceStat = []
        g_others = 0.0
        for deviceValue in self.sheet.deviceNameViewsPercent:
            if deviceValue[1] > threshold:
                globalDeviceStat.append({"device" : self.nameManufacturerMap[deviceValue[0]].upper() + " " +deviceValue[0], "value" : deviceValue[1]})
            else:
                g_others += deviceValue[1]        
        globalDeviceStat.append({"device" : "Others" , "value" : round(g_others,2)})
        self.globalInfo.append({"name" : "Global Device Stats", "value" : globalDeviceStat})
        self.globalInfo.append({"name" : "Total Linkedin views", "value" : self.sheet.total_views})
        self.globalInfo.append({"name":"Input Android Traffic - number of deviceType-os pairs", "value" : self.sheet.extraInfo["Input Android Traffic"]})
        self.globalInfo.append({"name":"Number of manufacturers supported by Google Play", "value" : androidNS.manufacturersGplay})
        self.globalInfo.append({"name":"Number of manufacturers non-Google-play", "value" : self.sheet.extraInfo["Number of unsupported google play manufacturers"]})
        self.globalInfo.append({"name":"Number of devices supported by Google Play", "value" : androidNS.googlePlayDevices})
        self.globalInfo.append({"name":"Number of non-Google-play devices for all OS versions", "value" : self.sheet.extraInfo["Number of unsupported google play devices"]})
        self.globalInfo.append({"name":"number of views with invalid os version (all versions)", "value" : self.sheet.extraInfo["Invalid os version related views"]    })
        self.globalInfo.append({"name":"Number of devices found with invalid OS version", "value" : self.sheet.extraInfo["Number of devices with invalid OS"]})


class IosStat():

    def __init__(self, inputData):
        
        self.sheet = Ios()
        self.global_views = 0.0

        for d in inputData[1:]:
            #try:
            self.sheet.insert(d)
            #except:
            #print "[ ERROR in parsing ]  ",d

        self.sheet.setupData()
        self.sheet.refactorOSversionList()
        for humanName in self.sheet.numOfViewsHuman:
            self.sheet.numOfViewsHumanPercent[humanName] = round((self.sheet.numOfViewsHuman[humanName]/self.sheet.global_views)*100, 2)
        self.sorted_global = sorted(self.sheet.numOfViewsHumanPercent.items(), key=operator.itemgetter(1), reverse=True)
        self.globalInfo = []
        self.setupGlobalData()

    def xStats(self,xOSversion,global_threshold,threshold, roundBy, osmax,osmin):

        result = []
        os_version_list = []
        if xOSversion == 'x':
            os_version_list = self.sheet.xlist
        elif xOSversion == 'xx':
            os_version_list = self.sheet.xxlist
        elif xOSversion == 'xxx':
            os_version_list = self.sheet.xxxlist
        else:
            os_version_list.append(xOSversion)
        print os_version_list

        deviceGroup = []
        osmax = int(osmax)
        osmin = int(osmin)
        os_others = 0.0
        os_results = dict()
        os_global_share = dict()
        for os_version in os_version_list:
            x, xx, xxx = processOsVersion(os_version)
            if xOSversion == 'xx':
                if xx is None:
                    continue
            if xOSversion == 'xxx':
                if xxx is None:
                    continue
            if (int(x) > osmax) or (int(x) < osmin):
                continue
            device_result = self.getDeviceStats(x,xx,xxx,threshold, roundBy)
            print device_result[0]
            processed_os_version = "{0}.{1}.{2}".format(x , xx if xx else "x" , xxx if xxx else "x")
            if device_result[0]['Global share of os'] < global_threshold:
                print "Skipped %s" % processed_os_version
                os_others += device_result[0]['Global share of os']
                continue
            os_results[processed_os_version] = device_result
            os_global_share[processed_os_version] = device_result[0]['Global share of os']
            #deviceGroup.append({"name": processed_os_version, "value" : device_result})
      

        sorted_os_results = sorted(os_global_share.items(), key=operator.itemgetter(1), reverse=True)
        for osresult in sorted_os_results:
            deviceGroup.append({osresult[0]: os_results[osresult[0]]})
        deviceGroup.append({"Global share of other OS in %s"%xOSversion : os_others})
        #deviceGroup.append({"Global share of other OS in %s"%xOSversion : os_others})

        result.append({"name" : "Device Stats - Query", "value" : deviceGroup})
        result.append({"name" : "Global Info", "value" : self.globalInfo})

        return {"Result":result}

    def getDeviceStats(self,x, xx, xxx,threshold, roundBy):

        dataValues = returnDictWithZeroValues(self.sheet.deviceMap)
        dataPercentages = returnDictWithZeroValues(self.sheet.deviceMap)

        for record in self.sheet.deviceRecords:
            if record.query_osVersion(x,xx,xxx):
                dataValues[record.name] += record.num_of_views

        summ = 0.0
        for key in dataValues:
            summ += dataValues[key]
        if summ==0:
            return {"Result" : "No Stats found"}

        for key,value in dataValues.iteritems():
            v = (value/summ)*100                 
            dataPercentages[key] = round(v,roundBy)


        sorted_devices = sorted(dataPercentages.items(), key=operator.itemgetter(1), reverse=True)
        sorted_device_share = []
        result = []
        percentTotal = 0.0
        others = 0.0
        for device in sorted_devices:
            percentTotal += device[1]
            if device[1] > 0.01:
                dev_list = []
                dev_list.append({"name" : device[0]})
                dev_list.append({"GlobalShare" : round((dataValues[device[0]]/self.sheet.global_views)*100,roundBy)})
                dev_list.append({"value" : device[1]})
                dev_list.append({"impressions" : dataValues[device[0]]})
                sorted_device_share.append({ "Device" : dev_list })
            else:
                others += device[1]
        dev_list = []
        dev_list.append({"name" : "others"})
        dev_list.append({"GlobalShare" : round((long(others*summ)/self.sheet.global_views)*100,roundBy)})
        dev_list.append({"value" : round(others, 4)})
        dev_list.append({"impressions" : long(others*summ)})

        sorted_device_share.append({"Device": dev_list})

        
        sorted_device_share.append({"device":"Others", "value":others})
        result.append({"Global share of os" : round((summ/self.sheet.global_views)*100,roundBy)})
        result.append({"name":"DeviceStats" , "value": sorted_device_share})
        result.append({"name":"Query for iOS version" , "value" : "{0}.{1}.{2}".format(x , xx if xx else "x" , xxx if xxx else "x")})
        result.append({"name":"Error in approximation" , "value": 100-percentTotal})

        return result

    def setupGlobalData(self,threshold=0.8):

        globalDeviceStat = []
        g_others = 0.0
        for deviceValue in self.sorted_global:
            if deviceValue[1] > threshold:
                globalDeviceStat.append({"device" : deviceValue[0], "value" : deviceValue[1]})
            else:
                g_others += deviceValue[1]        
        globalDeviceStat.append({"device" : "Others" , "value" : round(g_others,2)})
        self.globalInfo.append({"name" : "Global Device Stats", "value" : globalDeviceStat})
        self.globalInfo.append({"name" : "Total Linkedin views", "value" : self.sheet.global_views})
        self.globalInfo.append({"name":"Input IOS Traffic - number of deviceType-os pairs", "value" : len(self.sheet.deviceRecords)})

