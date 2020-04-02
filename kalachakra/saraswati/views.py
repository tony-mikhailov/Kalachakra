import calendar
import json
from builtins import object
from datetime import datetime

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import first
from django.urls import reverse
from django.utils.datetime_safe import strftime
from django.views.decorators.csrf import csrf_exempt
from yaml import serialize

import saraswati.cal_helpers
from saraswati.serializers import MoonDaySerializer
from saraswati.qol import date_conv

from .forms import RitualForm
from .models import Event, MoonDay, Ritual
from .qol import *


def index(request):
    if request.user.is_authenticated:

        return render(
            request,
            'index.html',
            context = {},
        )

    else :
        return HttpResponseRedirect('/accounts/login')


def today(request):
    day =  MoonDay.today()
    
    # morning_form = RitualForm(auto_id=True, initial = {'ritual' : day.morning_hural.pk, 'title' : 'Yarr'} )
    # day_form = RitualForm(auto_id=True, initial = {'ritual' : day.day_hural.pk} )
    
    ctx = { 'today': day}
    
    return render(request, 'today.html', context=ctx)

def today_json(request):
    # data = serializers.serialize("json", [MoonDay.today()], indent=2, ensure_ascii=False)
    data = json.dumps(MoonDay.today().json(), indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')

def day(request, year, month, day):
    
    day = MoonDay.year_day(year,month,day)
    
    morning_form = RitualForm(auto_id=True, initial = {'ritual' : day.morning_hural.pk } ) if day.morning_hural else None
    day_form = RitualForm(auto_id=True, initial = {'ritual' : day.day_hural.pk} ) if day.day_hural else None
    
    ctx = { 'today': day, 'morning_form' : morning_form, 'day_form' : day_form }
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
    
    
def day_json(request, year, month, day):
    yday = MoonDay.year_day(year,month,day)
    if request.method == 'POST':
        json_data = json.loads(request.body)
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
            # yday.moon_day_no = v
            # setattr(yday, 'moon_day_no_p', v-1)
        else:
            print ("%s:%s" % (k, v))
            setattr(yday, k, v)
        yday.save()
        return redirect(reverse('day_json', args=(year, month, day)))
    
    data = json.dumps(yday.json(), indent=2, ensure_ascii=False)
    
    return HttpResponse(data, content_type='application/json; charset=utf-8')

def delete_event(request, year, month, day):
    yday = MoonDay.year_day(year,month,day)
    if request.method == 'POST':
        j = json.loads(request.body)
        e = Event.objects.get(pk=j['id'])
        if e: e.delete()

    return redirect(reverse('day_json', args=(year, month, day)))
    # data = json.dumps(yday.json(), indent=2, ensure_ascii=False)
    # return HttpResponse(data, content_type='application/json; charset=utf-8')
        

def day_events_json(request, year, month, day):
    yday = MoonDay.year_day(year,month,day)
      
    arr=[]
    for e in yday.events.all():
        arr.append(e.json())  
    data = json.dumps(arr, indent=2, ensure_ascii=False)
    
    return HttpResponse(data, content_type='application/json; charset=utf-8')


def month(request, year, month):
    days_and_forms = []
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
    ctx = {'today': MoonDay.today(), 'days': days}
    return render(request, 'classic_month.html', context=ctx)

def month_json(request, year, month):
    ds = MoonDay.month_days(year, month)
    if request.method == 'POST':
        print ('process input month')
        return redirect(reverse('month_json', args=(year, month)))
    
    rarr = []
    for d in ds:
        rarr.append(d.json())
    data = json.dumps(rarr, indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')

def hurals_json(request):
    hs = Ritual.hurals()
    rarr = [{'id': None, "short_name": "нет хурала",}]
    for h in hs:
        rarr.append(h.json())
    
    data = json.dumps(rarr, indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')

def rituals_json(request):
    hs = Ritual.objects.all()
    rarr = [{'id': None, "short_name": "нет хурула"}]
    for h in hs:
        rarr.append(h.json())
    
    data = json.dumps(rarr, indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')


def ritual_json(request, id):
    r =  get_object_or_404(Ritual, pk=id)
    data = json.dumps(r.json(), indent=2, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json; charset=utf-8')
