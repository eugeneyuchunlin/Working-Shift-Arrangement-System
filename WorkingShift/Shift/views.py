from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
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

# Create your views here.
