# Generated by Django 4.2.4 on 2023-09-22 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multi_company', '0021_doisser_history'),
        ('leads', '0034_leadhistory_doisser'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='multi_company.company'),
        ),
    ]
