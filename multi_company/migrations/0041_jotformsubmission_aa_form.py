# Generated by Django 4.2.4 on 2023-10-20 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multi_company', '0040_jotform'),
    ]

    operations = [
        migrations.AddField(
            model_name='jotformsubmission_aa',
            name='form',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='multi_company.jotform'),
            preserve_default=False,
        ),
    ]
