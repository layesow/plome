# Generated by Django 4.2.4 on 2023-10-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0051_document_lead_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='document',
        ),
        migrations.AddField(
            model_name='lead',
            name='documents',
            field=models.ManyToManyField(blank=True, related_name='leads', to='leads.document'),
        ),
    ]
