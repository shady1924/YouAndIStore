from django.shortcuts import render
from django.http import HttpResponse
from empTimeSheet import models
from django.conf import settings
from django.http import JsonResponse
from copy import deepcopy
import datetime
# Create your views here.

def login(request):
    return render(request, 'empTimeSheet/login.html', context={'urlstr': settings.CONNURL})

def index(request):
    if request.user.is_authenticated:
        return render(request,'base.html')
    else:
        return HttpResponseBadRequest()

def uploadExcel(request):
    if request.user.is_authenticated:
        return render(request,'empTimeSheet/uploadExcel.html',  context={'urlstr' : settings.CONNURL} )
    else:
        return HttpResponseBadRequest()


def readAndSaveExcelData(request):
    print("Reading Excel Data!!", "Excel Name=",request.GET['filname'])
    # uncomments
    result = models.readParseSaveExcelData(request.GET['filname'])

    # result={'result': {'prem': 'Sheet:1,2,3 Days Absent:7, Days Worked:24', 'vipin': 'Sheet:1,2,3 Days Absent:6, Days Worked:25', 'manoj': 'Sheet:1,2,3 Days Absent:5, Days Worked:26', 'govind': 'Sheet:4,5,6 Days Absent:5, Days Worked:26', 'ritesh': 'Sheet:4,5,6 Days Absent:31, Days Worked:0', 'naveen': 'Sheet:4,5,6 Days Absent:3, Days Worked:28'}, 'err': []}
    print("readAndSaveExcelData:", result)
    # return HttpResponse(result, content_type="application/json")
    return render(request, 'empTimeSheet/uploadExcel.html',  context= {
        'dataset': result,
        'urlstr': settings.CONNURL
    })

def saveStoreConfig(request):
    print("request Called!!!! ")
    result = models.uploadShopConfig()
    print("Return object from views, saveStoreConfig : ", result)
    # return JsonResponse(result)
    return render(request, 'empTimeSheet/uploadExcel.html',  context= {
        'saveStoreConfigdataset': result,
        'urlstr': settings.CONNURL
    })

def CheckRetData(request):
    print("Reading Excel Data!!", "Excel Name=", request.GET['filname'])
    result = models.readParseSaveExcelData(request.GET['filname'])
    print("Model:", result)
    return HttpResponse(result, content_type="application/json")

def detailMonthlyReport(request):

    ## document from database returnobj = {'result', 'err': []}
    excelData = models.selectData(request.GET['monthStart'], request.GET['empname'])

    # print("Views detailMonthlyReport",excelData)

    ## format the data into proper sequence of columns in order to avoid issues in data table
    SummaryHeader = ['name', 'totalMonthlySalary', 'dailySalary', 'totalHolidaysAllowed', 'totalHolidaytaken',
                     'totalHolidaysWorked', 'totalSundaysAbsent',
                     'totalTimesLate', 'totaldeductions', 'totalAdditions', 'CalculatedSalary'
                     ]

    TimeHeader = ['day', 'dayOfWeek', 'shiftStart', 'shiftEnd', 'shiftWorkHours', 'shiftType', 'shiftComment',
                  'EmpTimeIn', 'EmpTimeOut', 'EnforcedEmpTimeIn', 'EnforcedEmpTimeOut',
                  'totalHoursLate', 'overTimeHours', 'Absent', 'halfDay', 'HolidayCredit', 'PercentSalaryAdditions',
                  'PercentDeductions', 'DailyAdditions', 'DailyDeductions'
                  ]
    temp = []

    result = {
        # "EmpSummary": {},
        "EmpSummary": [],
        # Get the daily attendance details in details element
        # "Details": excelData['result'][request.GET['empname']]['workhours'],
        "Details": [],
        "err": excelData['err']
    }

    if 'result' in excelData.keys():
        for key in SummaryHeader:
            temp.append(excelData['result'][request.GET['empname']][key])
        result["EmpSummary"].append(deepcopy(temp))
        del temp[:]

    monthlyArr = []

    dailyarr=excelData['result'][request.GET['empname']]['workhours']
    # print("dailyarr", dailyarr)

    if isinstance(dailyarr, list) and len(dailyarr) >1:
        for dayObj in dailyarr:
            for key in TimeHeader:
                temp.append(dayObj[key])
            result["Details"].append(deepcopy(temp))
            del temp[:]

    result["TimeHeader"] = TimeHeader
    result["SummaryHeader"] = SummaryHeader
    # if 'result' in excelData.keys():
    #     print("View: detailMonthlyReport", excelData['result'][request.GET['empname']])
    #     # Populate the summary/header information for the employee
    #     for key,val in excelData['result'][request.GET['empname']].items():
    #         print(type(key), type(val), key)
    #         if isinstance(val, str) or isinstance(val, float) or isinstance(val, int):
    #             result["EmpSummary"][key] = val

    # print(result)
    # return JsonResponse(result)
    return render(request, 'empTimeSheet/EmpSalaryDetailsModal.html', context={
        'dataset': result,
        'urlstr': settings.CONNURL
    })

def getComputedSalaryData(request):
    monthStart = request.GET.get('monthStart')
    if monthStart is None:
        # return HttpResponseBadRequest()
        return render(request, 'empTimeSheet/allEmpSalaryDetails.html', context={
            'urlstr': settings.CONNURL
        })
    else:
        monthStart=request.GET['monthStart']
        result=models.getComputedSalaryData(monthStart)
        # return HttpResponse(result, content_type="application/json"))
        # print("views: getComputedSalaryData", result)
        return render(request, 'empTimeSheet/allEmpSalaryDetails.html', context={
            'dataset': result,
            'urlstr': settings.CONNURL
        })

def getMonths(request):
    result=models.getMonths()
    print("getMonths view", result)
    # return HttpResponse(result, content_type="application/json")
    return JsonResponse(result)