# Generated by Django 4.2.4 on 2023-10-11 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multi_company', '0031_alter_jotformsubmission_date_debut_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jotformsubmission',
            name='date_debut',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='jotformsubmission',
            name='date_fin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='jotformsubmission',
            name='submission_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]