import json
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import utils 

def login(request):
    template = loader.get_template('Shift/login.html')
    return HttpResponse(template.render({},request))

def overview(request):
    rules = utils.getRule('rule2018')
    template = loader.get_template('Shift/overview.html')
    return HttpResponse(template.render(rules, request))

def shift(request):
    shift = utils.getShift('shift20185')
    template = loader.get_template('Shift/shift.html')
    return HttpResponse(template.render(shift, request))

@csrf_exempt
def postShift(request):
    data = json.loads(request.body, encoding=False)
    # step 1 : generate the current month calendar
    # step 2 : generate next month calendar
    # step 3 : calculate the shift
    # step 4 : update database
    return HttpResponse('Ok');

# Create your views here.
