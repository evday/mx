# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-16 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', max_length=300, verbose_name='\u8bb2\u5e08\u5efa\u8bae'),
        ),
        migrations.AddField(
            model_name='course',
            name='you_need_know',
            field=models.CharField(default='', max_length=300, verbose_name='\u8bfe\u7a0b\u987b\u77e5'),
        ),
    ]
