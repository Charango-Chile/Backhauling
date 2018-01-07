from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, StreamingHttpResponse
from .models import SysUsers
from .models import Truck
from django.template import loader
from .Test_PULP import main_run
import time
from .filters import TruckFilter
import json
import pandas as pd
import os

def adminlogin(request):
    template = loader.get_template('OptDemo/adminlogin.html')
    context = {}
    return HttpResponse(template.render(context, request))


def carrierlogin(request):
    template = loader.get_template('OptDemo/carrierlogin.html')
    context = {}
    return HttpResponse(template.render(context, request))


def shipperlogin(request):
    template = loader.get_template('OptDemo/shipperlogin.html')
    context = {}
    return HttpResponse(template.render(context, request))


def optlogin(request):
    EmailTMP = request.POST['Email'] #request.POST.get("Email")
    PasswordTMP = request.POST.get("Password")
    TypeTMP = request.POST['LoginType']
    Name = 'Not Found'
    List = SysUsers.objects.filter(Email__exact = EmailTMP).filter(Password__exact = PasswordTMP)

    context = {}
    template = loader.get_template('OptDemo/index.html')

    if TypeTMP == 'Admin':
        if len(List) > 0:
            Name = List[0].Name
            context = {
                'Login': EmailTMP,
                'Name': Name,
                'List': List,
                'Pwd': PasswordTMP,
            }
            template = loader.get_template('OptDemo/AdminEntry1.html')
        else:
            context = {}
            template = loader.get_template('OptDemo/index.html')

    if TypeTMP == 'Carrier':
        if len(List) > 0:
            Name = List[0].Name
            context = {
                'Login': EmailTMP,
                'Name': Name,
                'List': List,
                'Pwd': PasswordTMP,
            }
            template = loader.get_template('OptDemo/CarrierEntry.html')
        else:
            context = {}
            template = loader.get_template('OptDemo/index.html')

    if TypeTMP == 'Shipper':
        if len(List) > 0:
            Name = List[0].Name
            context = {
                'Login': EmailTMP,
                'Name': Name,
                'List': List,
                'Pwd': PasswordTMP,
            }
            template = loader.get_template('OptDemo/ShipperEntry.html')
        else:
            context = {}
            template = loader.get_template('OptDemo/index.html')

    return HttpResponse(template.render(context, request))


def optindex(request):
    template = loader.get_template('OptDemo/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def optregister(request):
    # TODO: Basado en el tipo de usuario, mandar a lo que corresponda
    TypeTMP = request.POST['LoginType']
    template = loader.get_template('OptDemo/index.html')
    context = {}

    if TypeTMP == 'Admin':
        template = loader.get_template('OptDemo/register_admin.html')
    if TypeTMP == 'Shipper':
        template = loader.get_template('OptDemo/register_shipper.html')
    if TypeTMP == 'Carrier':
        template = loader.get_template('OptDemo/register_carrier.html')

    return HttpResponse(template.render(context, request))


def optregister_conf(request):
    #TODO: Cambiar esto para agregar el tipo de usuario que registra
    EmailTMP = request.POST['Email']
    PasswordTMP = request.POST.get("Password")
    RepeatPwdTMP = request.POST.get("PasswordR")
    NameTMP = request.POST['Name']
    TypeTMP = request.POST['LoginType']


    template = loader.get_template('OptDemo/index.html')
    context = {}


    if TypeTMP == 'Admin':
        if PasswordTMP == RepeatPwdTMP:
            SysUsers.objects.create(Email=EmailTMP, Login='', Name=NameTMP, Password=PasswordTMP, Type=TypeTMP)
            template = loader.get_template('OptDemo/register_conf.html')
        else:
            template = loader.get_template('OptDemo/register_admin_error.html')
    if TypeTMP == 'Shipper':
        if PasswordTMP == RepeatPwdTMP:
            SysUsers.objects.create(Email=EmailTMP, Login='', Name=NameTMP, Password=PasswordTMP, Type=TypeTMP)
            template = loader.get_template('OptDemo/register_conf.html')
        else:
            template = loader.get_template('OptDemo/register_shipper_error.html')
    if TypeTMP == 'Carrier':
        if PasswordTMP == RepeatPwdTMP:
            SysUsers.objects.create(Email=EmailTMP, Login='', Name=NameTMP, Password=PasswordTMP, Type=TypeTMP)
            template = loader.get_template('OptDemo/register_conf.html')
        else:
            template = loader.get_template('OptDemo/register_carrier_error.html')



    return HttpResponse(template.render(context, request))


def adminentry(request, user_name):
    Truck_list = Truck.objects.all()
    Truck_filter = TruckFilter(request.GET, queryset=Truck_list)
    template = loader.get_template('OptDemo/AdminEntry.html')
    context = {'filter': Truck_filter, 'Name': user_name}
    return HttpResponse(template.render(context, request))

def carrierentry(request, user_name):
    template = loader.get_template('OptDemo/CarrierEntry.html')
    context = {'Name': user_name}
    return HttpResponse(template.render(context, request))

def shipperentry(request, user_name):
    template = loader.get_template('OptDemo/ShipperEntry.html')
    context = {'Name': user_name}
    return HttpResponse(template.render(context, request))


def optmatching(request, user_name):
    # main_run()
    template = loader.get_template('OptDemo/Matching.html')
    context = {'Name': user_name}
    return HttpResponse(template.render(context, request))

def optmatchres(request, user_name):
    while not os.path.exists('C:/Users/chara/Downloads/Distances.csv'):
        time.sleep(1)
    while not os.path.exists('C:/Users/chara/Downloads/TruckList.csv'):
        time.sleep(1)
    distancias = pd.read_csv('C:/Users/chara/Downloads/Distances.csv', header=None)
    trucks = pd.read_csv('C:/Users/chara/Downloads/TruckList.csv', header = None)
    os.remove('C:/Users/chara/Downloads/Distances.csv')
    os.remove('C:/Users/chara/Downloads/TruckList.csv')

    main_run(distancias, trucks)
    template = loader.get_template('OptDemo/Match_Res.html')
    context = {'Name': user_name}
    return HttpResponse(template.render(context, request))