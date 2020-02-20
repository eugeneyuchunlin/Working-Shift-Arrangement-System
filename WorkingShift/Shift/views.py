import json
import os
import csv
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from . import utils 

def login(request):
    template = loader.get_template('Shift/login.html')
    return HttpResponse(template.render({},request))

def overview(request):
    # check the query of year is legal
    print(request.GET)
    rules = utils.getRule(request.GET)
    if rules != None:
        months = utils.getCollection(request.GET['year'])
        rules['monthAttr'] = months
        template = loader.get_template('Shift/overview.html')
        return HttpResponse(template.render(rules, request))
    else:
        raise Http404("Overview Page Not Found")

def shift(request):
    # step 1 : check year and month is legal
    result = utils.checkYearMonthLegal(request.GET)
    if result != None:
        shift = utils.getShift('shift' + result['year'] + result['month'])
        template = loader.get_template('Shift/shift.html')
        return HttpResponse(template.render(shift, request))
    else:
        raise Http404("Shift Page Not Found")

@csrf_exempt
def postShift(request):
    year = request.GET['year']
    month = request.GET['month']
    data = json.loads(request.body, encoding=False)
    # step 1 : generate the current month calendar(csv)
    utils.generateTheCalendarCSV(data,year,month) 

    # step 2 : generate next month calendar(csv)
    utils.generateNextMonthCSV(year, month)

    # step 3 : generate holiday(csv)
    utils.generateHolidayCSV(data, year, month)

    # step 4 : calculate the shift
    utils.executeProgram(year, month)

    # step 5 : update database
    utils.updateDataBase(year,month)

    return shift(request)

# Create your views here.
