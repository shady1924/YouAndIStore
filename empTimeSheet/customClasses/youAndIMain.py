import os, sys
from .timesheet import Timesheet
from pathlib import Path
import pprint
from .dbConnect import dbConnect
from django.conf import settings
import json


def readExcelData(excelName):
    employeesData = {'result': {}, 'err': []}
    try:
        pp = pprint.PrettyPrinter(indent=4)
        workdir = settings.MEDIA_DIR
        timesheetObj = Timesheet(workdir)
        filename = os.path.join(settings.MEDIA_DIR, excelName)
        employeesData = timesheetObj.getSheetData(filename)

    except Exception as e:
        pp.pprint(e.args)
        pp.pprint(str(e))
        employeesData['err'].append('Error in parsing the Excel:readExcelData' + str(e))

    # pp.pprint(employeesData)

    if 'err' not in employeesData:
        try:
            computedSalaryDict = timesheetObj.applyBuinessRules(employeesData)
            ##save the computed salary into DB
            criteria = {
                "$and": [
                    {
                        "monthStart" : computedSalaryDict["monthStart"]
                    },
                    {
                        'monthEnd': computedSalaryDict["monthEnd"]
                    }
                ]
            }
            dbObj = dbConnect()
            DBResult = dbObj.searchUpdateAndInsert("empSalary", criteria, computedSalaryDict)

            if 'err' in DBResult.keys() and len(DBResult['err']) > 1:
                employeesData['err'].append(DBResult['err'])

        except Exception as e:
            if 'err' in computedSalaryDict.keys():
                employeesData['err'].append(computedSalaryDict['err'])
            print("applyBusinessRules Exception:", str(e))
            employeesData['err'].append(str(e))
    #
    # print("readExcelData", "\n\n\n Printing the compiled Salaries object!!!")
    # pp.pprint(employeesData)

    return employeesData

# upload the shop configuration data for the start end date for the shop as defined in the config file
def uploadShopConfigData():
    try:
        returnobj = {'updateConfigresult': {}, 'updateConfigErr': [], "empInfoUpdateResult": {}}
        pp = pprint.PrettyPrinter(indent=4)
        timesheetObj = Timesheet(settings.MEDIA_DIR)
        filename = os.path.join(settings.MEDIA_DIR, "shopConfig.xlsx")
        print(filename)
        shopHolidayConfigData, empDetailsData = timesheetObj.loadShopConfigData(filename)
        dbObj = dbConnect()
        ##Cleanup Old Collections
        result = {}
        result = dbObj.delRecord("shopConfiguration", {})
        result = dbObj.delRecord("empDetails", {})
        # Insert new data
        result = {}
        result = dbObj.updateCollection("shopConfiguration", shopHolidayConfigData)
        print("YouandIMain shopHolidayConfigData", shopHolidayConfigData)
        returnobj['updateConfigresult'] = result

        result = {}
        result = dbObj.updateCollection("empDetails", empDetailsData)
        print("YouandIMain empDetailsData", empDetailsData)
        returnobj['empInfoUpdateResult'] = result

    except Exception as e:
        pp.pprint(e.args)
        pp.pprint(sys.exc_info()[:2])
        returnobj['updateConfigErr'].append(' '.join(map(str, sys.exc_info()[:2])))

    return returnobj


## save the montly raw excel employee timesheet data into the database
def saveExcelData(excelName):
    returnobj = {'result': {}, 'err': []}
    pp = pprint.PrettyPrinter(indent=4)
    empTimesheetData = readExcelData(excelName)
    if 'err' in empTimesheetData:
        returnobj['err'].append(empTimesheetData['err'])
    else:
        try:

            criteria = {"$and": [
                    {'monthStart': empTimesheetData['monthStart']},
                    {'monthEnd': empTimesheetData['monthEnd']}
                ]
            }
            print(criteria)
            # Load into the database
            dbObj = dbConnect()
            DBResult = dbObj.searchUpdateAndInsert("emptimesheet", criteria, empTimesheetData)

            if len(DBResult['err']) > 1:
                returnobj['err'].append(DBResult['err'])

            insertedrec = {}
            for empname in empTimesheetData.keys():
                if isinstance(empTimesheetData[empname], dict):
                    print(empTimesheetData[empname]["sheet"], str(empTimesheetData[empname]["dayAbsence"]),
                          str(empTimesheetData[empname]["daysWorked"]))
                    insertedrec[empname] = {
                                            "Sheet" : empTimesheetData[empname]["sheet"] ,
                                            "Days Absent" : str(empTimesheetData[empname]["dayAbsence"]),
                                            "Days Worked" : str(empTimesheetData[empname]["daysWorked"])
                                            }

            insertedrec['monthStart'] = empTimesheetData['monthStart']
            insertedrec['monthEnd'] = empTimesheetData['monthEnd']

            pp.pprint(insertedrec)
            returnobj['result'] = insertedrec
        except Exception as e:
            pp.pprint(str(e))
            returnobj['err'].append("Exception in saveExcelData")
            returnobj['err'].append(str(e))
    return returnobj




