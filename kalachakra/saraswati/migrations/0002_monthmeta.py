# Generated by Django 2.2.6 on 2020-03-31 15:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saraswati', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=35)),
                ('no', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField(max_length=1080)),
            ],
        ),
    ]
