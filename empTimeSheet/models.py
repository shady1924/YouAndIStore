from django.db import models

# Create your models here.
from .customClasses.youAndIMain import saveExcelData
from .customClasses.youAndIMain import uploadShopConfigData
from .customClasses.dbConnect import dbConnect
from django.conf import settings
import json
import os
import copy
import pprint
from bson import json_util

def readParseSaveExcelData(excelName):
    returnStatus=saveExcelData(excelName)
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(returnStatus)
    # return json.dumps(returnStatus,indent=4, sort_keys=True, default=str)
    return returnStatus

def uploadShopConfig():
    returnStatus=uploadShopConfigData()
    pp = pprint.PrettyPrinter(indent=4)
    print("returnStatus", returnStatus)
    pp.pprint(returnStatus)
    return returnStatus

def selectData(monthStart, empname):
    pp = pprint.PrettyPrinter(indent=4)
    dbObj = dbConnect()

    collName = "empSalary"
    filters = {
        "monthStart": monthStart
    }

    projection = {'_id': 0, "monthStart": 1, empname: 1}
    dbResult = dbObj.getData(collName, filters, projection)
    return dbResult


def getComputedSalaryData(monthStart=None):
    collName = "empSalary"
    dbObj = dbConnect()
    filters = {
        "monthStart": monthStart
    }
    projection = {"_id": 0}
    dbResult = dbObj.getData(collName, filters, projection)
    if 'result' in dbResult:
        print("Model", "DBResult", type(dbResult), dbResult['result']['monthStart'])
    return dbResult

def getMonths():
    collName = "empSalary"
    dbObj = dbConnect()
    filters = {}
    projection = {"_id": 0, "monthStart": 1}
    result={
        "data" :[],
        "err": []
    }
    cnt=1

    retobj = dbObj.getDataArr(collName, filters, projection)
    if retobj['err'] and len(retobj['err']) > 1:
        result['err'] = retobj['err']

    # print("getMonths Models","retobj" ,retobj)

    for val in retobj['result']:
        # print("val", val, val['monthStart'])
        result["data"].append({ "id" : cnt,"text" :  val['monthStart']})
        cnt= cnt + 1
    print("Model", "result", result)
    return result