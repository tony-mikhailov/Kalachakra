import calendar
import json
from builtins import object
import datetime

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import first
from django.urls import reverse
from django.utils.datetime_safe import strftime
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from yaml import serialize
from django.utils.translation import get_language, activate
from django.template.defaultfilters import date
from django.contrib.auth import authenticate
from django.contrib import auth

from .forms import RitualForm
from .models import Event, MoonDay, Ritual
from .qol import *


def index(request):
    day = MoonDay.today()
    y=  day.year
    m= day.month()
    d= day.day()
    return common_month(request, y, m)

def edit(request):
    print ("try to edit")
    if request.user.is_authenticated:
        day = MoonDay.today()
        ctx = { 'today': day, }
        return common_month(request, y, m)
        # return HttpResponse(render(request, 'index.html', context=ctx), content_type='html; charset=utf-8')
    else:
        return HttpResponseRedirect('/accounts/login')

def today(request):
    day = MoonDay.today()
    ctx = { 'today': day, }
    return render(request, 'today.html', context=ctx)

def month(request):
    day = MoonDay.today()
    ctx = { 'today': day, }
    return render(request, 'month.html', context=ctx)

def today_json(request):
    # data = serializers.serialize("json", [MoonDay.today()], indent=2, ensure_ascii=False)
    data = json.dumps(MoonDay.today().json(), indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')

def day(request, year, month, day):
    
    day = MoonDay.year_day(year,month,day)
    
    
    ctx = { 'today': day}
    return render(request, 'today.html', context=ctx)

def process_event_json(event, day):
    print ("new event has come %s" % (event))
    ritual_id = None if (event['ritual_id'] == '') or (not event['ritual_id']) else int(event['ritual_id'])
    ritual = None if ritual_id == None else Ritual.objects.get(pk=ritual_id)
    
    bts=event['begin_time'] if event['begin_time'] else '00:00:00'
    ets=event['end_time'] if event['end_time'] else '00:00:00'
    bt=datetime.strptime(bts, '%H:%M:%S')
    et=datetime.strptime(ets, '%H:%M:%S')
    if 'id' in event:
        nevent = get_object_or_404(Event, pk=event['id'])
        nevent.begin_time=bt
        nevent.end_time=et
        nevent.title=event['title']
        nevent.description=event['description']
        # nevent.moonday=day
        nevent.article_link=event['article_link']
        nevent.ritual=ritual
    else:
        nevent = Event(
            begin_time=bt,
            end_time=et,
            title=event['title'],
            description=event['description'],
            moonday=day,
            article_link=event['article_link'],
            ritual=ritual,
        )

    nevent.save()
    
@csrf_exempt
def day_json(request, year, month, day):
    if not request.user.is_authenticated: return HttpResponseForbidden()

    yday = MoonDay.year_day(year,month,day)
    if request.method == 'POST':
        json_data = json.loads(request.body)
        # del json_data['sessionid']
        # del json_data['csrftoken']
        k=next(iter(json_data))
        v=json_data[k]
        
        if k == 'morning_hural_id':
            yday.morning_hural = get_or_none(Ritual, pk=v)
        elif k == 'day_hural_id':
            yday.day_hural = get_or_none(Ritual, pk=v)
        elif k == 'moon_day_no':
            yday.moon_day_no = v
            setattr(yday, 'moon_day_no_p', v-1)
        elif k == 'events':
            process_event_json(v, yday)
        else:
            print ("%s:%s" % (k, v))
            setattr(yday, k, v)
        yday.save()
        return redirect(reverse('saraswati:day_json', args=(year, month, day)))
    
    data = json.dumps(yday.json(), indent=2, ensure_ascii=False)
    
    return HttpResponse(data, content_type='application/json; charset=utf-8')

@csrf_exempt
def delete_event(request, year, month, day):
    yday = MoonDay.year_day(year,month,day)
    if request.method == 'POST':
        j = json.loads(request.body)
        e = Event.objects.get(pk=j['id'])
        if e: e.delete()

    return redirect(reverse('saraswati:day_json', args=(year, month, day)))
    # data = json.dumps(yday.json(), indent=2, ensure_ascii=False)
    # return HttpResponse(data, content_type='application/json; charset=utf-8')
        
@csrf_exempt
def day_events_json(request, year, month, day):
    yday = MoonDay.year_day(year,month)
    arr=[]
    for e in yday.events.all():
        arr.append(e.json())  
    data = json.dumps(arr, indent=2, ensure_ascii=False)
    
    return HttpResponse(data, content_type='application/json; charset=utf-8')


def month(request, year, month):
    qs = MoonDay.month_days(year, month)
    ctx = {'today': qs[0], 'days': qs }
    return render(request, 'month.html', context=ctx)

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]


def common_month(request, year, month):
    qs = MoonDay.month_days(year, month)
    days=[]
    for d in qs:
        days.append(d.json())  
              
    ctx = {
        'today': MoonDay.today(), 
        'days': days,
        'days_qs': qs, 
        'year': year, 
        'month': month_to_long(month),
        'moonday': MoonDay.moon_day_no,
        'f': [1,8,15,30],
        # 'ms': {1: '&#x1F311;', 8: '&#x1f313;', 15: '&#x1F315;',30 : '&#x1F311'},
        # 'ms2': ['&#x1F311;', '&#x1f313;', '&#x1F315;','&#x1F311']
        	

    }
    return render(request, 'classic_month.html', context=ctx)

# @csrf_exempt
def month_json(request, year, month):
    ds = MoonDay.month_days(year, month)
    if request.method == 'POST':
        print ('process input month')
        return redirect(reverse('sarasawati:month_json', args=(year, month)))
    
    rarr = []
    for d in ds:
        rarr.append(d.json())
    data = json.dumps(rarr, indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')


@csrf_exempt
def hurals_json(request):
    hs = Ritual.hurals()
    rarr = [{'id': None, "short_name": "Нет хурала"}]
    for h in hs:
        rarr.append(h.json())
    
    data = json.dumps(rarr, indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')

@csrf_exempt
def rituals_json(request):
    hs = Ritual.objects.all()
    rarr = [{'id': None, "short_name": "нет хурула"}]
    for h in hs:
        rarr.append(h.json())
    
    data = json.dumps(rarr, indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')


@csrf_exempt
def ritual_json(request, id):
    r =  get_object_or_404(Ritual, pk=id)
    data = json.dumps(r.json(), indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')


class ApiUser(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

    def __str__(self):
        return super().__str__()

@csrf_exempt
def api_login(request : HttpRequest):

    req_user = ApiUser(request.body)
    print (f'{req_user.login} {req_user.password}')

    user = authenticate(username=req_user.login, password=req_user.password)

    if user is None:
        # A backend authenticated the credentials
        return HttpResponseForbidden()
    else:
        auth.login(request, user)
        data = serializers.serialize("json", [user], indent=2, ensure_ascii=False)
        return HttpResponse(data, content_type="application/json", status=200)
        # auth.login(request, CustomUser.objects.get(username=req_user.username))


def api_logout(request : HttpRequest):
    auth.logout(request)
    data = "Bye..."
    return HttpResponse(data, content_type="text/plain", status=200)

def api_user(request : HttpRequest):
    
    if request.user.is_anonymous: 
        data = "{\"user\":\"nouser\"}"
    else:
        data = serializers.serialize("json", [request.user], indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type="application/json", status=200)
