

from datetime import *


def noneOrPk(inp):
    return inp.pk if inp else None


def date_check(year,month,day):
    try:
        datetime.strptime('%d-%d-%d'%(year,month,day), '%Y-%m-%d')
        return True
    except ValueError:
        return False

def date_conv(year,month,day):
    return datetime.strptime('%d-%d-%d'%(year,month,day), '%Y-%m-%d')

def serialize_ritual(ritual):
    from .serializers import RitualSerializer
    return RitualSerializer(ritual).data

def serialize_moonday(moonday):
    from .serializers import MoonDaySerializer
    return MoonDaySerializer(moonday).data

def serialize_event(event):
    from .serializers import EventSerializer
    return EventSerializer(event).data

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
