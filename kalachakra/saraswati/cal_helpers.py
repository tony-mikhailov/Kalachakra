from .models import MoonDay, Ritual
from datetime import *



def clear_year(year):
    return MoonDay.objects.filter(year=year).delete()

def fill_default_calendar(year, save=False):
    days = MoonDay.objects.filter(year=year)
    fd = datetime(year, 1, 1)
    ld = datetime(year+1,1,1)
    dd = ld-fd
    
    sdn=0
    sdmn=6 
    
    for i in range(sdn, dd.days):
        nmd = MoonDay(year=year, day_no=i, moon_day_no=sdmn, morning_hural=Ritual.objects.get(pk=13), day_hural=Ritual.objects.get(pk=14))
        if nmd.date().weekday() == 4:
            nmd.day_hural = Ritual.objects.get(pk=16) # юроол
        elif nmd.date().weekday() == 5:
            nmd.day_hural = Ritual.objects.get(pk=17) # банзарагша
        elif nmd.date().weekday() == 6:
            nmd.morning_hural = Ritual.objects.get(pk=15) # намсарай
            nmd.day_hural = Ritual.objects.get(pk=18) # алтэн гэрэл
            tl = [(25, 31),(23, 29),(25, 31),(24, 30),(25, 31),(24, 30),(25, 31),(25, 31), (24, 30),(25, 31),(24, 30),(25, 31)] if dd.days == 366 else [(25, 31),(22, 28),(25, 31),(24, 30),(25, 31),(24, 30),(25, 31),(25, 31), (24, 30),(25, 31),(24, 30),(25, 31)]            
            if nmd.date().day in range(tl[nmd.date().month-1][0], tl[nmd.date().month-1][1]):
                nmd.day_hural = Ritual.objects.get(pk=19) # сундуй
                
        sdmn = sdmn + 1 if sdmn < 29 else 1
        
        if save: 
            nmd.save()
        print (str(nmd))

    return days