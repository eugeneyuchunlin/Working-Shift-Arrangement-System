import json
import os
import csv
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from . import utils 

def get_client_ip(request):
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60 
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)


def loginPage(request):
    template = loader.get_template('Shift/login.html')
    return HttpResponse(template.render({},request))

@csrf_exempt
def login(request):
    data = json.loads(request.body)
    if utils.checkLogin(data):
        # must set the cookie value
        # In the next version, I'll set the cookie feature just because I'm lazy
        response  = HttpResponse('Ok')
        return response
    else:
        return HttpResponse('Not Ok')

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
    quality = utils.uploadQuality(result['year'], result['month'])
    if result != None:
        shift = utils.getShift('shift' + result['year'] + result['month'])
        shift['year'] = result['year']
        shift['mon'] = request.GET['month']
        shift['quality'] = quality
        template = loader.get_template('Shift/shift.html')
        return HttpResponse(template.render(shift, request))
    else:
        raise Http404("Shift Page Not Found")

@csrf_exempt
def postShift(request):
    # check post mode
    year = request.GET['year']
    month = request.GET['month']
    mode = request.GET['mode']
    data = json.loads(request.body, encoding=False)

    if mode == 'computing':
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
    elif mode == 'saving':
        utils.saveShift(data, year, month)
        return HttpResponse('Ok') 

def saveShift(request):
    year = request.GET['year']
    month = request.GET['month']
    data = json.loads(request.body, encoding='utf-8')
    utils.saveShift(data, year, month);
    # save data to the database
    return HttpResponse('Ok')
# Create your views here.
