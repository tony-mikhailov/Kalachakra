from django.db import models

from datetime import *
import calendar

from django.db import models
from django.db.models.sql import where
from django.utils.translation import ugettext_lazy as _
from .qol import *

from django.core.validators import MaxValueValidator, MinValueValidator



class MonthMeta(models.Model):
    title = models.CharField(max_length=35)
    no = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(12), MinValueValidator(1)]
    )
    description = models.TextField(max_length=1080)
    

    
class Ritual(models.Model):
    short_name = models.CharField(max_length=35)
    long_name = models.TextField(max_length=108)
    people_name = models.TextField(max_length=108, null=True, blank=True, default=None)
    is_hural = models.BooleanField(default=True)
    celebration_hural = models.BooleanField(default=False)
    for_best_reincarnation = models.BooleanField(default=False)
    note_allowed = models.BooleanField(default=True)
    note_for_one_name = models.BooleanField(default=False)
    note_fix_price = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    description_link = models.URLField(null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    bg_color = models.CharField(
        verbose_name=_(u'Background Color'), 
        max_length=7,
        help_text=_(u'HEX color, as #RRGGBB'), 
        null=True, blank=True
    )
    fg_color = models.CharField(
        verbose_name=_(u'Foreground Color'), 
        max_length=7,
        help_text=_(u'HEX color, as #RRGGBB'), 
        null=True, blank=True
    )
    
    def __str__(self):
        return "%s" % (self.short_name)

    def json(self):
        return serialize_ritual(self)

    @staticmethod
    def hurals():
        return Ritual.objects.filter(is_hural=True);
    

#todo: add day events, rename morning_hural to hural1, hural2

class MoonDay(models.Model):
    year = models.IntegerField()
    day_no = models.IntegerField()
    moon_day_no = models.IntegerField()
    
    morning_hural = models.ForeignKey(Ritual, related_name='morning2ritual', on_delete=models.CASCADE, null=True, blank=True)
    day_hural = models.ForeignKey(Ritual,related_name='day2ritual', on_delete=models.CASCADE, null=True, blank=True)

    morning_hural_comment = models.TextField(null=True, blank=True, default=None)
    day_hural_comment = models.TextField(null=True, blank=True, default=None)
        
    baldjinima = models.BooleanField(default=False)
    dashinima = models.BooleanField(default=False)
    tersuud = models.BooleanField(default=False)
    modon_hohimoy = models.BooleanField(default=False)
    riha = models.BooleanField(default=False)
    pagshag = models.BooleanField(default=False)
    good_for_haircut = models.BooleanField(default=False)
    good_for_travel = models.BooleanField(default=False)
    significant_day = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)
    article_link = models.URLField(null=True, blank=True)     
    lamas_checked = models.BooleanField(default=False)
    bg_color = models.CharField(
        verbose_name=_(u'Background Color'), 
        max_length=7,
        help_text=_(u'HEX color, as #RRGGBB'),
        null=True, blank=True
    )
    fg_color = models.CharField(
        verbose_name=_(u'Foreground Color'), 
        max_length=7,
        help_text=_(u'HEX color, as #RRGGBB'), 
        null=True, blank=True
    )


    @property
    def moon_day_no_p(self):
        return self.moon_day_no
    
    @moon_day_no_p.setter
    def moon_day_no_p(self, value):
        if value:
            future_days = MoonDay.objects.filter(year=self.year, day_no__gte=self.day_no)
            i0 = value
            for futday in future_days:
                i0 = i0 + 1 if i0 < 30 else 1
                futday.moon_day_no = i0
                # print("%d"%(futday.moon_day_no))
                futday.save()

    @staticmethod
    def today():
        td = date.today()
        return MoonDay.objects.get(year=td.year, day_no=td.timetuple().tm_yday-1)
    
    @staticmethod
    def month_days(year, month):
        (fd, ld) = (date(year=year,month=month, day=1), date(year=year,month=month, day=calendar.monthrange(year, month)[1]))
        (fd_no, ld_no) = (fd.timetuple().tm_yday-1, ld.timetuple().tm_yday-1)
        return MoonDay.objects.filter(year=year,day_no__gte=fd_no,day_no__lte=ld_no)

    @staticmethod
    def year_day(year, month, day):
        date = date_conv(year,month,day)
        day = MoonDay.objects.get(year=year,day_no=date.timetuple().tm_yday-1)
        return day


    def __str__(self):
        return "%s" % (self.date_str())

    def tm_day(self):
        td = date.fromordinal(self.date().toordinal()+1)
        return td.timetuple().tm_mday

    def tm_month(self):
        td = date.fromordinal(self.date().toordinal()+1)
        return td.timetuple().tm_mon
    
    def tm_year(self):
        td = date.fromordinal(self.date().toordinal()+1)
        return td.timetuple().tm_year

    def ys_day(self):
        td = date.fromordinal(self.date().toordinal()-1)
        return td.timetuple().tm_mday

    def ys_month(self):
        td = date.fromordinal(self.date().toordinal()-1)
        return td.timetuple().tm_mon
    
    def ys_year(self):
        td = date.fromordinal(self.date().toordinal()-1)
        return td.timetuple().tm_year

    def tomorrow(self):
        td = date.today()+1
        return MoonDay.objects.get(year=td.year, day_no=td.timetuple().tm_yday-1)

    def yesterday(self):
        td = date.today()-1
        return MoonDay.objects.get(year=td.year, day_no=td.timetuple().tm_yday-1)
    

    def date(self):
        fd = datetime(self.year, 1, 1)
        rd = fd + timedelta(days=self.day_no)
        return rd

    def date_str(self):
        return self.date().strftime("%Y-%m-%d")

    def month(self):
        return int(self.date().strftime("%m"))

    def month_fullname(self):
        return self.date().strftime("%B")

    def day(self):
        return int(self.date().strftime("%d"))

    def weekday(self):
        return self.date().weekday()

    
    def url(self):
        from django.urls import reverse
        return reverse('day', args=[str(self.year), self.month(), self.day() ])
    
    def json(self):
        return serialize_moonday(self)
        
class Event(models.Model):
    begin_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=108, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    article_link = models.URLField(null=True, blank=True)     
    video_link = models.URLField(null=True, blank=True)     
    moonday = models.ForeignKey(MoonDay, related_name='events', on_delete=models.CASCADE, null=True, blank=True)
    ritual = models.ForeignKey(Ritual, related_name='events', on_delete=models.CASCADE, null=True, blank=True)

    bg_color = models.CharField(
        verbose_name=_(u'Background Color'), 
        max_length=7,
        help_text=_(u'HEX color, as #RRGGBB'), 
        null=True, blank=True
    )
    fg_color = models.CharField(
        verbose_name=_(u'Foreground Color'), 
        max_length=7,
        help_text=_(u'HEX color, as #RRGGBB'), 
        null=True, blank=True
    )


    def json(self):
        return serialize_event(self)
    
    def __str__(self):
        return "%s; %s; %s; %s; %s" % (str(self.begin_time), str(self.end_time), str(self.description), str(self.article_link), str(self.ritual_id))
    
