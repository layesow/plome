# Generated by Django 4.2.4 on 2023-09-22 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_customusertypes_can_fetch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customusertypes',
            name='company',
        ),
    ]
