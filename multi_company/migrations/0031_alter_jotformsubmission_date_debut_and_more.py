# Generated by Django 4.2.4 on 2023-10-11 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multi_company', '0030_alter_jotformsubmission_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jotformsubmission',
            name='date_debut',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jotformsubmission',
            name='date_fin',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
