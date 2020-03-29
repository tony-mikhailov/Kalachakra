from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Ritual, MoonDay, Event

class RitualResource(resources.ModelResource):
    class Meta:
        model = Ritual

class MoonDayResource(resources.ModelResource):
    class Meta:
        model = MoonDay

class EventResource(resources.ModelResource):
    class Meta:
        model = Event


class RitualAdmin(ImportExportModelAdmin):
    resource_class = RitualResource

class MoonDayAdmin(ImportExportModelAdmin):
    resource_class = MoonDayResource

class EventAdmin(ImportExportModelAdmin):
    resource_class = EventResource


admin.site.register(Ritual, RitualAdmin)
admin.site.register(MoonDay, MoonDayAdmin)
admin.site.register(Event, EventAdmin)
