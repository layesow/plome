# Generated by Django 4.2.4 on 2023-10-20 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multi_company', '0038_jotformsubmission_data_json'),
    ]

    operations = [
        migrations.CreateModel(
            name='JotFormSubmission_aa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.TextField(blank=True, null=True)),
                ('first_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('signature', models.TextField(blank=True, null=True)),
                ('numero_telephone', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('choix_formation', models.TextField(blank=True, null=True)),
                ('date_debut', models.TextField(blank=True, null=True)),
                ('date_fin', models.TextField(blank=True, null=True)),
                ('nombre_heure', models.TextField(blank=True, null=True)),
                ('prix_formation', models.TextField(blank=True, null=True)),
                ('passage_au', models.TextField(blank=True, null=True)),
                ('votre_conseiller', models.TextField(blank=True, null=True)),
                ('formation', models.TextField(blank=True, null=True)),
                ('audio_appel_qualite', models.TextField(blank=True, null=True)),
                ('audio_suivi_formation', models.TextField(blank=True, null=True)),
                ('data_json', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
