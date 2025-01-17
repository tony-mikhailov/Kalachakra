

from rest_framework import serializers

from saraswati.models import MoonDay, Ritual, Event
from .qol import noneOrPk


class RitualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ritual
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id_from_event')
    ritual_id = serializers.SerializerMethodField('get_ritual_id_from_event')

    class Meta:
        model = Event
        fields = ['begin_time','end_time','title','description','article_link','moonday','id','ritual_id']

    def get_ritual_id_from_event(self, event):
        return event.ritual_id

    def get_id_from_event(self, event):
        return event.pk


class MoonDaySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url_from_moonday')
    weekday = serializers.SerializerMethodField('get_weekday_from_moonday')
    date = serializers.SerializerMethodField('get_date_from_moonday')
    month = serializers.SerializerMethodField('get_month_from_moonday')
    day = serializers.SerializerMethodField('get_day_from_moonday')

    morning_hural_id = serializers.SerializerMethodField('get_morning_hural_from_moonday')
    day_hural_id = serializers.SerializerMethodField('get_day_hural_from_moonday')
    events = serializers.SerializerMethodField('get_events_from_moonday')
    
    class Meta:
        model = MoonDay
        fields = ['year','month','day','day_no','moon_day_no','morning_hural_id','day_hural_id','url','weekday','date','month','baldjinima','dashinima','tersuud','modon_hohimoy','riha','pagshag','good_for_haircut','good_for_travel','significant_day','comment','article_link','lamas_checked','events']
        
    def get_url_from_moonday(self, moonday):
        return moonday.url()

    def get_weekday_from_moonday(self, moonday):
        return moonday.weekday() + 1

    def get_date_from_moonday(self, moonday):
        return moonday.date_str()

    def get_month_from_moonday(self, moonday):
        return moonday.month()

    def get_day_from_moonday(self, moonday):
        return moonday.day()


    def get_morning_hural_from_moonday(self, moonday):
        return noneOrPk(moonday.morning_hural)

    def get_day_hural_from_moonday(self, moonday):
        return noneOrPk(moonday.day_hural)

    def get_events_from_moonday(self, moonday):
        arr=[]
        for e in moonday.events.all():
            arr.append(e.json())  
        return arr

