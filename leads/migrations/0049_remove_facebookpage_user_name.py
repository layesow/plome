# Generated by Django 4.2.4 on 2023-10-04 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0048_facebookpage_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebookpage',
            name='user_name',
        ),
    ]
