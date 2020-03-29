from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Transaction


class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction

class TransactionAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource


admin.site.register(Transaction, TransactionAdmin)
