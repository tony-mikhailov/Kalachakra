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

    def formfield_for_dbfield(self, db_field, **kwargs):
        from widgets import ColorPickerWidget
        if db_field.name.contains('color'):
            kwargs['widget'] = ColorPickerWidget
        return super(Room, self).formfield_for_dbfield(db_field, **kwargs)


class EventResource(resources.ModelResource):
    class Meta:
        model = Event


class RitualAdmin(ImportExportModelAdmin):
    resource_class = RitualResource

#class MoonDayAdmin(ImportExportModelAdmin):

class EventAdmin(ImportExportModelAdmin):
    resource_class = EventResource



admin.site.register(Ritual, RitualAdmin)
admin.site.register(Event, EventAdmin)


class MoonDayAdmin(ImportExportModelAdmin):
    # list_display = ('title', 'color', 'is_active', 'reg_datetime')
    resource_class = MoonDayResource

    # ordering = ('title', )
    # search_fields = ('title',)
    # fieldsets = ((None, {'fields': ('title', 'color', 'is_active')}),)


    
# admin.site.register(Room, MoonDayAdmin)
admin.site.register(MoonDay, MoonDayAdmin)

# admin.site.register(Ritual)
# admin.site.register(MoonDay)

