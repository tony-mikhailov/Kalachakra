from django.db import models

from datetime import *

from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.db.models.sql import where
from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import BooleanField

from greentara.qol import *

class Transaction(models.Model):
    created_at = models.DateTimeField(verbose_name=_(u'Creation date time'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_(u'Update date time'), auto_now=True)
    status = models.CharField(max_length=35, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    pid = models.CharField(max_length=40)
    amount = models.IntegerField(
        default=10,
        validators=[
            MaxValueValidator(100000000),
            MinValueValidator(10)
        ]
    )
    currency = models.CharField(max_length=5)
    saved = models.BooleanField()
    canceled = models.BooleanField()
    cancel_wait = models.BooleanField()
    from_vk = models.BooleanField()
    description = models.TextField(null=True, blank=True)
    short_bank_info = models.CharField(max_length=200)
    next_pay = models.DateTimeField(verbose_name=_(u'Next payment date time for saved paymemts'))
    last_pay_status = models.CharField(max_length=35)
    last_mailed_at = models.DateTimeField(verbose_name=_(u'Last sended email date time'), auto_now_add=True)
    note_subj = models.CharField(max_length=80, null=True, blank=True)
    note_data = models.TextField(null=True, blank=True)
    pay_ref = models.CharField(max_length=16)
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    attempts_count = models.PositiveIntegerField(default = 0)
