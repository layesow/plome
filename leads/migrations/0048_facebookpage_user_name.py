# Generated by Django 4.2.4 on 2023-10-04 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0047_alter_facebookpage_page_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookpage',
            name='user_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
