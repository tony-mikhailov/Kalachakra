# Generated by Django 2.2.6 on 2020-04-05 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saraswati', '0003_auto_20200402_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='ritual',
            name='people_name',
            field=models.TextField(blank=True, default=None, max_length=108, null=True),
        ),
    ]
