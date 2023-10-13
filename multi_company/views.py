from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
import pandas as pd
from .models import Doisser
from django.contrib import messages
import datetime
from leads.models import Company 

from django.shortcuts import render, redirect
from .models import FormSettings
from leads.models import Company

def create_form_settings(request):
    if request.method == 'POST':
        company_id = request.POST.get('company')
        form_name = request.POST.get('form_name')

        if company_id and form_name:
            company = Company.objects.get(id=company_id)
            form_settings = FormSettings(company=company, form_name=form_name)
            form_settings.save()
            return redirect('')  # Redirect to a success page or your desired URL

    companies = Company.objects.all()
    return render(request, 'multi_company/create_form_settings.html', {'companies': companies})


def doisser(request):
    records = Doisser.objects.all()
    companies = Company.objects.all()
    selected_company_id = request.GET.get('company_id')
    
    # Apply the company filter
    if selected_company_id:
        try:
            selected_company = Company.objects.get(id=selected_company_id)
            records = records.filter(company=selected_company)
        except Company.DoesNotExist:
            pass

    return render(request, 'multi_company/doisser.html', {'records': records, 'companies': companies})


def check_input_type(input_str):
    input_str = input_str.strip()
    
    formats = [
        ("%d-%m-%Y", "%Y-%m-%d"),
        ("%d-%m-%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"),
        ("%d-%m-%Y %H:%M", "%Y-%m-%d %H:%M:%S"),
        ("%Y-%m-%d %H:%M:%S", None),
        ("%Y-%m-%d", None),
        ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"),
        ("%d/%m/%Y", "%Y-%m-%d")
    ]
    
    for pattern, output_format in formats:
        try:
            date_obj = datetime.datetime.strptime(input_str, pattern)
            return date_obj.strftime(output_format) if output_format else input_str
        except ValueError:
            pass
    
    return "1900-01-01 00:00:00" if not input_str else "Invalid"


def import_doisser_leads(request):
    if request.method == 'POST':
        csv_file = request.FILES['excel_file']
        
        # df = pd.read_excel(csv_file)
        df = pd.read_csv(csv_file)
        column_mapping  = {
            "A" : "date_dinscription",
            "B" : "numero_edof",
            "C" : "nom",
            "D" : "prenom",
            "E" : "telephone",
            "F" : "mail",
            "G" : "address_postal",
            "H" : "colis_a_preparer",
            "I" : "statut_edof",
            "J" : "challenge",
            "K" : "prix_net",
            "L" : "conseiller",
            "M" : "equipes",
            "N" : "criteres_com",
            "O" : "date_prevue_d_entree_en_formation",
            "P" : "date_prevue_de_fin_de_formation",
            "Q" : "appel_effectue_le_date_time",
            "W" : "appel_effectue_le_motifs",
            "U" : "rdv_confirme_dateandtime",
            "S" : "rdv_confirme_confirmateur",
            "T" : "rdv_confirme_statut_service_confirmateur",
            "Z" : "inscription_visio_entree_audio",
            "AA" : "inscription_visio_entree_niveau_de_relance",
            "AD" : "inscription_visio_entree_somme_facturee",
            "AE" : "inscription_visio_entree_date_de_facturation",
            "AF" : "inscription_visio_entree_date_d_encaissement",
            "AB" : "inscription_visio_entree_facture",
            "AC" : "inscription_visio_entree_num_facture",
            "AG" : "inscription_visio_entree_colis_a_envoyer_le",
            "AI" : "inscription_visio_entree_numero_de_suivi_vers_point_relais",
            "AJ" : "inscription_visio_entree_commentaires",
            "AH" : "inscription_visio_entree_statut_colis",
        }
        df.rename(columns=column_mapping, inplace=True)
        df.fillna("", inplace=True)
        
        for _, row in df.iterrows():
            date_dinscription = check_input_type(row['date_dinscription'])
            numero_edof = int(row['numero_edof'].strip()) if row['numero_edof'].strip().isdigit() else None

            # numero_edof=row['numero_edof']
            nom=row['nom']
            prenom=row['prenom']
            telephone = int(row['telephone']) if row['telephone'].isdigit() else None if row['telephone'] else None
            mail=row['mail']
            address_postal=row['address_postal']
            statut_edof=row['statut_edof']
            challenge=row['challenge']
            colis_a_preparer=row['colis_a_preparer']
            prix_net=row['prix_net'] if row['prix_net'] else None
            conseiller=row['conseiller']
            equipes=row['equipes']
            criteres_com=row['criteres_com'] if row['criteres_com'] else None
            date_prevue_d_entree_en_formation=check_input_type(row['date_prevue_d_entree_en_formation'])
            date_prevue_de_fin_de_formation=check_input_type(row['date_prevue_de_fin_de_formation'])
            appel_effectue_le_date_time = check_input_type(row['appel_effectue_le_date_time'])
            appel_effectue_le_motifs=check_input_type(row['appel_effectue_le_motifs'])
            rdv_confirme_dateandtime=check_input_type(row['rdv_confirme_dateandtime'])
            rdv_confirme_confirmateur=row['rdv_confirme_confirmateur']
            rdv_confirme_statut_service_confirmateur=row['rdv_confirme_statut_service_confirmateur']
            inscription_visio_entree_audio=row['inscription_visio_entree_audio']
            inscription_visio_entree_niveau_de_relance=row['inscription_visio_entree_niveau_de_relance']
            inscription_visio_entree_somme_facturee=row['inscription_visio_entree_somme_facturee'] if row['inscription_visio_entree_somme_facturee'] else None 
            inscription_visio_entree_date_de_facturation=check_input_type(row['inscription_visio_entree_date_de_facturation'])
            inscription_visio_entree_date_d_encaissement=check_input_type(row['inscription_visio_entree_date_d_encaissement'])
            inscription_visio_entree_facture=row['inscription_visio_entree_facture']
            inscription_visio_entree_num_facture=row['inscription_visio_entree_num_facture']
            inscription_visio_entree_colis_a_envoyer_le=check_input_type(row['inscription_visio_entree_colis_a_envoyer_le'])
            inscription_visio_entree_numero_de_suivi_vers_point_relais=row['inscription_visio_entree_numero_de_suivi_vers_point_relais']
            inscription_visio_entree_commentaires=row['inscription_visio_entree_commentaires']
            inscription_visio_entree_statut_colis=row['inscription_visio_entree_statut_colis']


            Doisser_data = Doisser(
                date_dinscription = date_dinscription,
                numero_edof = numero_edof,
                nom = nom,
                prenom = prenom,
                telephone = telephone,
                mail = mail,
                address_postal = address_postal,
                statut_edof = statut_edof,
                challenge = challenge,
                colis_a_preparer = colis_a_preparer,
                prix_net = prix_net,
                conseiller = conseiller,
                equipes = equipes,
                criteres_com = criteres_com,
                date_prevue_d_entree_en_formation = date_prevue_d_entree_en_formation,
                date_prevue_de_fin_de_formation = date_prevue_de_fin_de_formation,
                appel_effectue_le_date_time = appel_effectue_le_date_time,
                appel_effectue_le_motifs = appel_effectue_le_motifs,
                rdv_confirme_dateandtime = rdv_confirme_dateandtime,
                rdv_confirme_confirmateur = rdv_confirme_confirmateur,
                rdv_confirme_statut_service_confirmateur = rdv_confirme_statut_service_confirmateur,
                inscription_visio_entree_audio = inscription_visio_entree_audio,
                inscription_visio_entree_niveau_de_relance = inscription_visio_entree_niveau_de_relance,
                inscription_visio_entree_somme_facturee = inscription_visio_entree_somme_facturee,
                inscription_visio_entree_date_de_facturation = inscription_visio_entree_date_de_facturation,
                inscription_visio_entree_date_d_encaissement = inscription_visio_entree_date_d_encaissement,
                inscription_visio_entree_facture = inscription_visio_entree_facture,
                inscription_visio_entree_num_facture = inscription_visio_entree_num_facture,
                inscription_visio_entree_colis_a_envoyer_le = inscription_visio_entree_colis_a_envoyer_le,
                inscription_visio_entree_numero_de_suivi_vers_point_relais = inscription_visio_entree_numero_de_suivi_vers_point_relais,
                inscription_visio_entree_commentaires = inscription_visio_entree_commentaires,
                inscription_visio_entree_statut_colis = inscription_visio_entree_statut_colis
            )
            Doisser_data.save()
        return redirect('doisser')
    else:
        Doisserdata = Doisser.objects.all()
        return render(request, 'mutli_company/doisser.html', context={"Doisserdata" : Doisserdata})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Formation
from django.http import JsonResponse

def edit_formation(request, formation_id):
    formation = get_object_or_404(Formation, pk=formation_id)

    if request.method == "POST":
        # Update formation fields
        formation.date_de_soumission = request.POST.get('editDate')
        formation.nom_de_la_campagne = request.POST.get('editCampagne')
        formation.nom_prenom = request.POST.get('editNomPrenom')
        formation.telephone = request.POST.get('editTelephone')
        formation.email = request.POST.get('editEmail')
        formation.comments = request.POST.get('editComments')
        formation.price = request.POST.get('editPrice')
        formation.conseiller = request.POST.get('editConseiller')

        # Handle custom fields
        custom_fields = {}
        for key, value in request.POST.items():
            if key.startswith('editCustomField_'):
                field_number = key.split('_')[-1]
                custom_field_name = value
                custom_field_data = request.POST.get(f'editCustomFieldData_{field_number}')
                custom_fields[custom_field_name] = custom_field_data

        formation.custom_fields = custom_fields
        formation.save()

        return redirect('edit_formation')  # Redirect to the list of formations after editing

    return render(request, 'multi_company/edit_formation.html', {'formation': formation})



def edit_doisser_lead(request, pid=None):
    if request.method == 'POST':
        edit_data = get_object_or_404(Doisser, pk=pid)
        # Fetch the company instance based on the provided company_id from the form
        company_id = request.POST.get('company_id', None)
        try:
            company = Company.objects.get(id=company_id) if company_id else None
        except Company.DoesNotExist:
            company = None  # Handle the case when the company doesn't exist

        date_dinscription = request.POST.get('date_dinscription', None)
        numero_edof = request.POST.get('numero_edof', None)
        nom = request.POST.get('nom', None)
        prenom = request.POST.get('prenom', None)
        telephone = request.POST.get('telephone', None)
        mail = request.POST.get('mail', None)
        address_postal = request.POST.get('address_postal', None)
        statut_edof = request.POST.get('statut_edof', None)
        challenge = request.POST.get('challenge', None)
        colis_a_preparer = request.POST.get('colis_a_preparer', None)
        prix_net = request.POST.get('prix_net', None)
        conseiller = request.POST.get('conseiller', None)
        equipes = request.POST.get('equipes', None)
        criteres_com = request.POST.get('criteres_com', None)
        date_prevue_d_entree_en_formation = request.POST.get('date_prevue_d_entree_en_formation', None)
        date_prevue_de_fin_de_formation = request.POST.get('date_prevue_de_fin_de_formation', None)
        appel_effectue_le_date_time = request.POST.get('appel_effectue_le_date_time', None)
        appel_effectue_le_motifs = request.POST.get('appel_effectue_le_motifs', None)
        rdv_confirme_dateandtime = request.POST.get('rdv_confirme_dateandtime', None)
        rdv_confirme_confirmateur = request.POST.get('rdv_confirme_confirmateur', None)
        rdv_confirme_statut_service_confirmateur = request.POST.get('rdv_confirme_statut_service_confirmateur', None)
        inscription_visio_entree_audio = request.POST.get('inscription_visio_entree_audio', None)
        inscription_visio_entree_niveau_de_relance = request.POST.get('inscription_visio_entree_niveau_de_relance', None)
        inscription_visio_entree_somme_facturee = request.POST.get('inscription_visio_entree_somme_facturee', None)
        inscription_visio_entree_date_de_facturation = request.POST.get('inscription_visio_entree_date_de_facturation', None)
        inscription_visio_entree_date_d_encaissement = request.POST.get('inscription_visio_entree_date_d_encaissement', None)
        inscription_visio_entree_facture = request.POST.get('inscription_visio_entree_facture', None)
        inscription_visio_entree_num_facture = request.POST.get('inscription_visio_entree_num_facture', None)
        inscription_visio_entree_colis_a_envoyer_le = request.POST.get('inscription_visio_entree_colis_a_envoyer_le', None)
        inscription_visio_entree_numero_de_suivi_vers_point_relais = request.POST.get('inscription_visio_entree_numero_de_suivi_vers_point_relais', None)
        inscription_visio_entree_commentaires = request.POST.get('inscription_visio_entree_commentaires', None)
        inscription_visio_entree_statut_colis = request.POST.get('inscription_visio_entree_statut_colis', None)

        # 
        edit_data.date_dinscription=date_dinscription
        edit_data.company = company
        edit_data.numero_edof=numero_edof
        edit_data.nom=nom
        edit_data.prenom=prenom
        edit_data.telephone=telephone
        edit_data.mail=mail
        edit_data.address_postal=address_postal
        edit_data.statut_edof=statut_edof
        edit_data.challenge=challenge
        edit_data.colis_a_preparer=colis_a_preparer
        edit_data.prix_net=prix_net
        edit_data.conseiller=conseiller
        edit_data.equipes=equipes
        edit_data.criteres_com=criteres_com
        edit_data.date_prevue_d_entree_en_formation=date_prevue_d_entree_en_formation
        edit_data.date_prevue_de_fin_de_formation=date_prevue_de_fin_de_formation
        edit_data.appel_effectue_le_date_time=appel_effectue_le_date_time
        edit_data.appel_effectue_le_motifs=appel_effectue_le_motifs
        edit_data.rdv_confirme_dateandtime=rdv_confirme_dateandtime
        edit_data.rdv_confirme_confirmateur=rdv_confirme_confirmateur
        edit_data.rdv_confirme_statut_service_confirmateur=rdv_confirme_statut_service_confirmateur
        edit_data.inscription_visio_entree_audio=inscription_visio_entree_audio
        edit_data.inscription_visio_entree_niveau_de_relance=inscription_visio_entree_niveau_de_relance
        edit_data.inscription_visio_entree_somme_facturee=inscription_visio_entree_somme_facturee
        edit_data.inscription_visio_entree_date_de_facturation=inscription_visio_entree_date_de_facturation
        edit_data.inscription_visio_entree_date_d_encaissement=inscription_visio_entree_date_d_encaissement
        edit_data.inscription_visio_entree_facture=inscription_visio_entree_facture
        edit_data.inscription_visio_entree_num_facture=inscription_visio_entree_num_facture
        edit_data.inscription_visio_entree_colis_a_envoyer_le=inscription_visio_entree_colis_a_envoyer_le
        edit_data.inscription_visio_entree_numero_de_suivi_vers_point_relais=inscription_visio_entree_numero_de_suivi_vers_point_relais
        edit_data.inscription_visio_entree_commentaires=inscription_visio_entree_commentaires
        edit_data.inscription_visio_entree_statut_colis=inscription_visio_entree_statut_colis

        edit_data.save()
        return redirect('doisser')
    else:
        viewdata = get_object_or_404(Doisser, pk=pid)
        companies = Company.objects.all()
        return render(request, 'mutli_company/edit_dossier_data.html', {"viewdata" : viewdata, "companies": companies})


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Doisser

# Your parse_date function here

def add_doisser_lead(request):
    if request.method == 'POST':
        # Get form data
        date_dinscription = check_input_type(request.POST.get('date_dinscription', '1900-01-01 00:00:00'))
        numero_edof = request.POST.get('numero_edof', None)
        nom = request.POST.get('nom', None)
        prenom = request.POST.get('prenom', None)
        telephone = int(request.POST.get('telephone')) if request.POST.get('telephone').isdigit() else None
        mail = request.POST.get('mail', None)
        address_postal = request.POST.get('address_postal', None)
        statut_edof = request.POST.get('statut_edof', None)
        challenge = request.POST.get('challenge', None)
        colis_a_preparer = request.POST.get('colis_a_preparer', None)
        prix_net = float(request.POST.get('prix_net', 0.0))
        criteres_com = float(request.POST.get('criteres_com', 0.0))
        date_prevue_d_entree_en_formation = check_input_type(request.POST.get('date_prevue_d_entree_en_formation', '1900-01-01 00:00:00'))
        date_prevue_de_fin_de_formation = check_input_type(request.POST.get('date_prevue_de_fin_de_formation', '1900-01-01 00:00:00'))
        appel_effectue_le_date_time = check_input_type(request.POST.get('appel_effectue_le_date_time', '1900-01-01 00:00:00'))
        appel_effectue_le_motifs = request.POST.get('appel_effectue_le_motifs', None)
        rdv_confirme_dateandtime = check_input_type(request.POST.get('rdv_confirme_dateandtime', '1900-01-01 00:00:00'))
        rdv_confirme_confirmateur = request.POST.get('rdv_confirme_confirmateur', None)
        rdv_confirme_statut_service_confirmateur = request.POST.get('rdv_confirme_statut_service_confirmateur', None)
        inscription_visio_entree_audio = request.POST.get('inscription_visio_entree_audio', None)
        inscription_visio_entree_niveau_de_relance = request.POST.get('inscription_visio_entree_niveau_de_relance', None)
        inscription_visio_entree_somme_facturee = float(request.POST.get('inscription_visio_entree_somme_facturee', 0.0))
        inscription_visio_entree_date_de_facturation = check_input_type(request.POST.get('inscription_visio_entree_date_de_facturation', '1900-01-01 00:00:00'))
        inscription_visio_entree_date_d_encaissement = check_input_type(request.POST.get('inscription_visio_entree_date_d_encaissement', '1900-01-01 00:00:00'))
        inscription_visio_entree_facture = request.POST.get('inscription_visio_entree_facture', None)
        inscription_visio_entree_num_facture = request.POST.get('inscription_visio_entree_num_facture', None)
        inscription_visio_entree_numero_de_suivi_vers_point_relais = request.POST.get('inscription_visio_entree_numero_de_suivi_vers_point_relais', None)
        inscription_visio_entree_commentaires = request.POST.get('inscription_visio_entree_commentaires', None)
        inscription_visio_entree_statut_colis = request.POST.get('inscription_visio_entree_statut_colis', None)
        # Handle JSONField separately (assuming it's sent as JSON in the POST request)
        custom_fields = request.POST.get('custom_fields', None)

        # Create a new Doisser Lead record with default values for empty fields
        doisser_lead = Doisser(
            date_dinscription=date_dinscription,
            numero_edof=numero_edof,
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            mail=mail,
            address_postal=address_postal,
            statut_edof=statut_edof,
            challenge=challenge,
            colis_a_preparer=colis_a_preparer,
            prix_net=prix_net,
            criteres_com=criteres_com,
            date_prevue_d_entree_en_formation=date_prevue_d_entree_en_formation,
            date_prevue_de_fin_de_formation=date_prevue_de_fin_de_formation,
            appel_effectue_le_date_time=appel_effectue_le_date_time,
            appel_effectue_le_motifs=appel_effectue_le_motifs,
            rdv_confirme_dateandtime=rdv_confirme_dateandtime,
            rdv_confirme_confirmateur=rdv_confirme_confirmateur,
            rdv_confirme_statut_service_confirmateur=rdv_confirme_statut_service_confirmateur,
            inscription_visio_entree_audio=inscription_visio_entree_audio,
            inscription_visio_entree_niveau_de_relance=inscription_visio_entree_niveau_de_relance,
            inscription_visio_entree_somme_facturee=inscription_visio_entree_somme_facturee,
            inscription_visio_entree_date_de_facturation=inscription_visio_entree_date_de_facturation,
            inscription_visio_entree_date_d_encaissement=inscription_visio_entree_date_d_encaissement,
            inscription_visio_entree_facture=inscription_visio_entree_facture,
            inscription_visio_entree_num_facture=inscription_visio_entree_num_facture,
            inscription_visio_entree_numero_de_suivi_vers_point_relais=inscription_visio_entree_numero_de_suivi_vers_point_relais,
            inscription_visio_entree_commentaires=inscription_visio_entree_commentaires,
            inscription_visio_entree_statut_colis=inscription_visio_entree_statut_colis,
            custom_fields=custom_fields,  # Handle JSONField
        )
        doisser_lead.save()

        # Redirect to the page where you want to display the Doisser Leads list
        return redirect('doisser')

    # If the request is not a POST request, simply render the page
    return render(request, 'multi_company/doisser.html')




from django.shortcuts import render, get_object_or_404
from leads.models import Lead
from leads.models import LeadHistory  # Import the LeadHistory model

def doisser_detail(request, doisser_id):
    # Retrieve the Doisser object
    doisser = get_object_or_404(Doisser, id=doisser_id)

    # Retrieve the lead history for this Doisser
    lead_history = LeadHistory.objects.filter(doisser=doisser).order_by('-timestamp')

    context = {
        'doisser': doisser,
        'lead_history': lead_history,
    }

    return render(request, 'multi_company/doisser.html', context)

from django.shortcuts import render, redirect
from .models import Formation

def add_formation(request):
    if request.method == "POST":
        # Extract data from standard fields
        date_de_soumission = request.POST.get('date_de_soumission')
        nom_de_la_campagne = request.POST.get('nom_de_la_campagne')
        nom_prenom = request.POST.get('nom_prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        comments = request.POST.get('comments')
        price = request.POST.get('price')
        conseiller = request.POST.get('conseiller')

        # Create a dictionary for custom fields
        custom_fields = {}

        # Iterate over posted custom field names and data
        for key, value in request.POST.items():
            if key.startswith('custom_field_name_'):
                field_number = key.split('_')[-1]
                custom_field_name = value
                custom_field_data = request.POST.get(f'custom_field_data_{field_number}')
                custom_fields[custom_field_name] = custom_field_data

        # Create a Formation instance and save it
        formation = Formation(
            date_de_soumission=date_de_soumission,
            nom_de_la_campagne=nom_de_la_campagne,
            nom_prenom=nom_prenom,
            telephone=telephone,
            email=email,
            comments=comments,
            price=price,
            conseiller=conseiller,
            custom_fields=custom_fields
        )
        formation.save()
        
        

        return redirect('add_formation') 
    
   

    return render(request, 'multi_company/formation.html')

import requests
import re
import datetime
from django.shortcuts import render
from .models import JotFormSubmission
from django.shortcuts import render
from .models import JotFormSubmission

def show_jotform_data(request):
    # Retrieve all data from the JotFormSubmission model
    jotform_submissions = JotFormSubmission.objects.all()
    
    # Pass the data to a template for rendering
    return render(request, 'multi_company/jotform_reselform.html', {'jotform_submissions': jotform_submissions})


# views.py
import requests
import re
import datetime
from django.shortcuts import render
from .models import JotFormSubmission
from django.core.exceptions import ValidationError

def import_jotform_data(request):
    if request.method == 'POST':
        api_key = '210c836a9974c7a935312b1ea8943c90'  # Replace with your actual JotForm API key
        formId = '222203090268952'  # Replace with the actual form ID you want to retrieve
        max_records_per_request = 500

        all_records = []
        offset = 0
        while True:
            url = f'https://reselform.jotform.com/API/form/{formId}/submissions?apiKey={api_key}&limit={max_records_per_request}&offset={offset}'
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Request failed with status code: {response.status_code}")
                print(response.text)
                break

            try:
                table_data = response.json()
                content = table_data['content']

                if not content:
                    break

                for entry in content:
                    first_name = entry['answers']['4']['answer'].get('first', '')
                    last_name = entry['answers']['4']['answer'].get('last', '')
                    email = entry['answers']['7']['answer']
                    signature = entry['answers']['5'].get('answer', '')
                    numero_telephone = entry['answers'].get('6', {}).get('answer', '')

                    address = entry['answers'].get('8', {})
                    numero_et_rue = address.get('Numéro et rue', '')
                    complement_adresse = address.get('Complément d\'adresse', '')
                    ville = address.get('Ville', '')
                    etat_region = address.get('État/Région', '')
                    code_postal = address.get('Code Postal', '')

                    choix_formation = entry['answers']['11']['answer'][0]
                    start_date = entry['answers']['14'].get('answer', '')
                    end_date = entry['answers']['15'].get('answer', '')

                    nombre_heure = entry['answers'].get('24', '')
                    prix_formation = entry['answers'].get('20', '')
                    passage_au = entry['answers'].get('21', {}).get('answer', '')
                    votre_conseiller = entry['answers'].get('18', 'Vide')
                    formation = entry['answers'].get('19', [])
                    audio_appel_qualite = entry['answers'].get('27', [])
                    audio_suivi_formation = entry['answers'].get('28', [])

                    submission = JotFormSubmission(
                        submission_date=entry['created_at'],
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        signature=signature,
                        numero_telephone=numero_telephone,
                        numero_et_rue=numero_et_rue,
                        complement_adresse=complement_adresse,
                        ville=ville,
                        etat_region=etat_region,
                        code_postal=code_postal,
                        choix_formation=choix_formation,
                        date_debut=start_date,
                        date_fin=end_date,
                        nombre_heure=nombre_heure,
                        prix_formation=prix_formation,
                        passage_au=passage_au,
                        votre_conseiller=votre_conseiller,
                        formation=', '.join(formation),
                        audio_appel_qualite=', '.join(audio_appel_qualite),
                        audio_suivi_formation=', '.join(audio_suivi_formation),
                    )

                    try:
                        submission.full_clean()
                        submission.save()
                        all_records.append(submission)
                    except ValidationError:
                        print(f"*******************************************************Validation Error for Entry: {entry}")

                    offset += max_records_per_request

            except ValueError as e:
                print("Error decoding JSON response:", e)
                break

        print("Data imported and saved to the database.")

    jotform_submissions = JotFormSubmission.objects.all()

    return render(request, 'multi_company/jotform_reselform.html', {'jotform_submissions': jotform_submissions})




# def import_jotform_data(request):
#     if request.method == 'POST':
#         # Replace 'your_api_key_here' with your actual JotForm API key
#         api_key = '210c836a9974c7a935312b1ea8943c90'

#         # Replace 'your_table_id_here' with the actual table ID you want to retrieve
#         formId = '230664959653974'
        
#         max_records_per_request = 200
        
#           # Initialize a list to store all records
#         all_records = []
#         offset = 0
    
#         while True:

#             # Define the API endpoint URL
#             url = f'https://reselform.jotform.com/API/form/{formId}/submissions?apiKey={api_key}'

#             # Make a GET request to the JotForm API
#             response = requests.get(url)

#             if response.status_code == 200:
#                 try:
#                     table_data = response.json()
#                     content = table_data['content']
#                     # If there are no more records, exit the loop
#                     if not content:
#                         break

#                     for entry in content:
#                         submission_date = check_input_type(entry['created_at'])
#                         first_name = entry['answers']['4']['answer']['first']
#                         last_name = entry['answers']['4']['answer']['last']
#                         email = entry['answers']['7']['answer']
#                         signature = entry['answers']['5'].get('answer', '')
#                         numero_telephone = None  # You can change this to the actual field
#                         if '6' in entry['answers'] and entry['answers']['6']['answer']:
#                             numero_telephone = entry['answers']['6']['answer']

#                         address_details = entry['answers']['8']['prettyFormat']
#                         address_match = re.search(
#                             r'Numéro et rue:(.*?)<br>Ville:(.*?)<br>État/Région:(.*?)<br>Code Postal:(\d+)', address_details)

#                         if address_match:
#                             numero_et_rue = address_match.group(1).strip()
#                             ville = address_match.group(2).strip()
#                             etat_region = address_match.group(3).strip()
#                             code_postal = address_match.group(4).strip()
#                         else:
#                             numero_et_rue = ''
#                             ville = ''
#                             etat_region = ''
#                             code_postal = ''

#                         formation = entry['answers']['11']['answer'][0]
#                         start_date = check_input_type(entry['answers']['14']['prettyFormat'])
#                         end_date = check_input_type(entry['answers']['15']['prettyFormat'])

#                         # Create and save a JotFormSubmission instance
#                         submission = JotFormSubmission(
#                             submission_date=submission_date,
#                             first_name=first_name,
#                             last_name=last_name,
#                             email=email,
#                             signature=signature,
#                             telephone=numero_telephone,
#                             numero_et_rue=numero_et_rue,
#                             ville=ville,
#                             etat_region=etat_region,
#                             code_postal=code_postal,
#                             choix_formation=formation,
#                             date_debut=start_date,
#                             date_fin=end_date,
#                         )
#                         submission.save()
#                         all_records.append(submission)
#                     offset += max_records_per_request

#                     print("Data imported and saved to the database.")
#                 except ValueError as e:
#                     print("Error decoding JSON response:", e)
#                     break
#             else:
#                 print(f"Request failed with status code: {response.status_code}")
#                 print(response.text)  # Print the response content for debugging

#         jotform_submissions = JotFormSubmission.objects.all()  # Assuming you have a model named JotFormSubmission
#         print(jotform_submissions)  # Debug print statement


#     # Render the template
#     return render(request, 'multi_company/jotform_reselform.html',{'jotform_submissions': jotform_submissions})


# @login_required
# def lead_history_view(request, lead_id):
#     lead = get_object_or_404(Doisser, id=lead_id)
#     lead_history = LeadHistory.objects.filter(lead=lead, category='mention').order_by('-timestamp')[:10]
#     return render(request, 'lead/lead_history.html', {'lead': lead, 'history_entries': lead_history})



# def import_doisser_leads(request):
#     field_map = {
#         'date_dinscription': 'Date d\'inscription',
#         'numero_edof': 'Numéro EDOF',
#         'nom': 'Nom',
#         'prenom': 'Prénom',
#         'telephone': 'Numéro de téléphone',
#         'mail': 'Mail',
#         'address_postal': 'Adresse Postale',
#         'statut_edof': 'Statut EDOF',
#         'challenge': 'Chalenge',
#         'colis_a_preparer': 'Colis à Préparer',
#         'prix_net': 'Prix Net',
#         'conseiller': 'Conseiller',
#         'equipes': 'Équipes',
#         'criteres_com': 'Critères com',
#         'date_prevue_d_entree_en_formation': 'Date Prévue d\'entrée en Formation',
#         'date_prevue_de_fin_de_formation': 'Date Prévue de Fin de Formation',
        
#         # Fields from AppelEffectueLe model
#         'appel_effectue_le_date_time': 'Date/Heure de l\'appel effectué',
#         'appel_effectue_le_motifs': 'Motifs de l\'appel effectué',
        
#         # Fields from RdvConfirme model
#         'rdv_confirme_dateandtime': 'Date/Heure du RDV confirmé',
#         'rdv_confirme_confirmateur': 'Confirmateur du RDV',
#         'rdv_confirme_statut_service_confirmateur': 'Statut du service du confirmateur du RDV',
        
#         # Fields from InscriptionVisioEntree model
#         'inscription_visio_entree_audio': 'Audio lors de l\'inscription à la visio',
#         'inscription_visio_entree_niveau_de_relance': 'Niveau de relance lors de l\'inscription à la visio',
#         'inscription_visio_entree_somme_facturee': 'Somme facturée lors de l\'inscription à la visio',
#         'inscription_visio_entree_date_de_facturation': 'Date de facturation lors de l\'inscription à la visio',
#         'inscription_visio_entree_date_d_encaissement': 'Date d\'encaissement lors de l\'inscription à la visio',
#         'inscription_visio_entree_facture': 'Facture lors de l\'inscription à la visio',
#         'inscription_visio_entree_num_facture': 'Numéro de facture lors de l\'inscription à la visio',
#         'inscription_visio_entree_colis_a_envoyer_le': 'Date de colis à envoyer lors de l\'inscription à la visio',
#         'inscription_visio_entree_numero_de_suivi_vers_point_relais': 'Numéro de suivi vers le point relais lors de l\'inscription à la visio',
#         'inscription_visio_entree_commentaires': 'Commentaires lors de l\'inscription à la visio',
#         'inscription_visio_entree_statut_colis': 'Statut du colis lors de l\'inscription à la visio',
#     }

#     if request.method == 'POST':
#         if 'file' in request.FILES:
#             file = request.FILES['file']
#             try:
#                 if file.name.endswith('.xls') or file.name.endswith('.xlsx'):
#                     df = pd.read_excel(file)
#                 else:
#                     raise ValueError("Unsupported file format. Only XLS and XLSX files are allowed.")

#                 headers = [header.strip() for header in df.columns]
#                 field_map_normalized = {key.lower().replace(" ", "_"): value for key, value in field_map.items()}
#                 filtered_headers = [header for header in headers if header.lower() in field_map_normalized.values()]

#                 additional_headers = [header for header in headers if header.lower() not in field_map_normalized.values()]
#                 filtered_headers_lower = [header.lower() for header in filtered_headers]
#                 filtered_field_map = {key: value for key, value in field_map.items() if value in filtered_headers_lower}

#                 df_dict = df.to_dict(orient='records')
#                 json_data = json.dumps(df_dict, default=date_handler)
#                 request.session['df'] = json_data
#                 request.session['field_map'] = field_map

#                 context = {'headers': headers, 'field_map': field_map, 'additional_headers': additional_headers}
#                 return render(request, 'multi_company/mapping_dossier_modal.html', context)
#             except Exception as e:
#                 messages.error(request, f'Error reading file: {str(e)}')
#                 return redirect('doisser')

#         elif 'mapping' in request.POST:
#             mapping_data = {}
#             custom_fields = {}

#             for field, field_name in field_map.items():
#                 mapping_data[field] = request.POST.get(field, '')

#             for custom_field in request.POST.getlist('custom_fields'):
#                 custom_fields[custom_field] = custom_field

#             mapping_data.update({'custom_fields': custom_fields})

#             df_records = request.session.get('df', [])
#             field_map = request.session.get('field_map', {})

#             leads = []
#             for record in json.loads(df_records):
#                 lead_data = {}
#                 for header, field in mapping_data.items():
#                     if field == '__empty__':
#                         value_holder = None
#                     elif header == 'custom_fields':
#                         custom_f = {}
#                         for excess_key, excess_fields in field.items():
#                             excess_value = record.get(excess_key)
#                             excess_value_holder = None
#                             if (isinstance(excess_value, float) and math.isnan(excess_value)) or excess_value == 'NaT':
#                                 excess_value_holder = ''
#                             else:
#                                 excess_value_holder =  excess_value
#                             custom_f[excess_key] = excess_value_holder
#                         lead_data['custom_fields'] = custom_f
#                     else:
#                         value = record.get(field)
#                         value_holder = None
#                         if header.startswith('date_'):
#                             date_value = parse_date(value)
#                             value_holder = date_value if not pd.isna(date_value) else None
#                         elif isinstance(value, float) and math.isnan(value):
#                             value_holder = ''
#                         elif isinstance(value, float) and not math.isnan(value):
#                             value_holder = int(value) if value.is_integer() else value
#                         else:
#                             value_holder = record[field]

#                         lead_data[header] = value_holder

#                 leads.append(Doisser(**lead_data))

#             Doisser.objects.bulk_create(leads)
#             request.session.pop('df', None)
#             request.session.pop('field_map', None)

#             messages.success(request, f'{len(leads)} leads imported successfully.')

#             return redirect('doisser')

#     return redirect('doisser')


# def import_doisser_leads(request):
#     field_map = {
#         'date_dinscription': 'Date d\'inscription',
#         'numero_edof': 'Numéro EDOF',
#         'nom': 'Nom',
#         'prenom': 'Prénom',
#         'telephone': 'Numéro de téléphone',
#         'mail': 'Mail',
#         'address_postal': 'Adresse Postale',
#         'statut_edof': 'Statut EDOF',
#         'challenge': 'Chalenge',
#         'colis_a_preparer': 'Colis à Préparer',
#         'prix_net': 'Prix Net',
#         'conseiller': 'Conseiller',
#         'equipes': 'Équipes',
#         'criteres_com': 'Critères com',
#         'date_prevue_d_entree_en_formation': 'Date Prévue d\'entrée en Formation',
#         'date_prevue_de_fin_de_formation': 'Date Prévue de Fin de Formation',
#     }
    
#     if request.method == 'POST':
#         if 'file' in request.FILES:
#             file = request.FILES['file']
#             try:
#                 if file.name.endswith('.xls') or file.name.endswith('.xlsx'):
#                     df = pd.read_excel(file)
#                 else:
#                     raise ValueError("Unsupported file format. Only XLS and XLSX files are allowed.")

#                 headers = [header.strip() for header in df.columns]
#                 field_map_normalized = {key.lower().replace(" ", "_"): value for key, value in field_map.items()}
#                 filtered_headers = [header for header in headers if header.lower() in field_map_normalized.values()]

#                 additional_headers = [header for header in headers if header.lower() not in field_map_normalized.values()]
#                 filtered_headers_lower = [header.lower() for header in filtered_headers]
#                 filtered_field_map = {key: value for key, value in field_map.items() if value in filtered_headers_lower}

#                 df_dict = df.to_dict(orient='records')
#                 json_data = json.dumps(df_dict, default=date_handler)
#                 request.session['df'] = json_data
#                 request.session['field_map'] = field_map

#                 context = {'headers': headers, 'field_map': field_map, 'additional_headers': additional_headers}
#                 return render(request, 'multi_company/mapping_dossier_modal.html', context)
#             except Exception as e:
#                 messages.error(request, f'Error reading file: {str(e)}')
#                 return redirect('doisser')

#         elif 'mapping' in request.POST:
#             mapping_data = {}
#             custom_fields = {}

#             for field, field_name in field_map.items():
#                 mapping_data[field] = request.POST.get(field, '')

#             for custom_field in request.POST.getlist('custom_fields'):
#                 custom_fields[custom_field] = custom_field

#             mapping_data.update({'custom_fields': custom_fields})

#             df_records = request.session.get('df', [])
#             field_map = request.session.get('field_map', {})

#             leads = []
#             for record in json.loads(df_records):
#                 lead_data = {}
#                 for header, field in mapping_data.items():
#                     if field == '__empty__':
#                         value_holder = None
#                     elif header == 'custom_fields':
#                         custom_f = {}
#                         for excess_key, excess_fields in field.items():
#                             excess_value = record.get(excess_key)
#                             excess_value_holder = None
#                             if (isinstance(excess_value, float) and math.isnan(excess_value)) or excess_value == 'NaT':
#                                 excess_value_holder = ''
#                             else:
#                                 excess_value_holder =  excess_value
#                             custom_f[excess_key] = excess_value_holder
#                         lead_data['custom_fields'] = custom_f
#                     else:
#                         value = record.get(field)
#                         value_holder = None
#                         if header.startswith('date_'):
#                             date_value = parse_date(value)
#                             value_holder = date_value if not pd.isna(date_value) else None
#                         elif isinstance(value, float) and math.isnan(value):
#                             value_holder = ''
#                         elif isinstance(value, float) and not math.isnan(value):
#                             value_holder = int(value) if value.is_integer() else value
#                         else:
#                             value_holder = record[field]

#                         lead_data[header] = value_holder

#                 leads.append(Doisser(**lead_data))

#             Doisser.objects.bulk_create(leads)
#             request.session.pop('df', None)
#             request.session.pop('field_map', None)

#             messages.success(request, f'{len(leads)} leads imported successfully.')

#             return redirect('doisser')

#     return redirect('doisser')




# # # multi_company/views.py
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from accounts.models import CustomUserTypes
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import User











# def import_doisser_leads(request):
#     field_map = {
#         'date_dinscription': 'Date d\'inscription',
#         'numero_edof': 'Numéro EDOF',
#         'nom': 'Nom',
#         'prenom': 'Prénom',
#         'telephone': 'Numéro de téléphone',
#         'mail': 'Mail',
#         'address_postal': 'Adresse Postale',
#         'statut_edof': 'Statut EDOF',
#         'challenge': 'Chalenge',
#         'colis_a_preparer': 'Colis à Préparer',
#         'prix_net': 'Prix Net',
#         'conseiller': 'Conseiller',
#         'equipes': 'Équipes',
#         'criteres_com': 'Critères com',
#         'date_prevue_d_entree_en_formation': 'Date Prévue d\'entrée en Formation',
#         'date_prevue_de_fin_de_formation': 'Date Prévue de Fin de Formation',
#     }
    
#     if request.method == 'POST':
#         if 'file' in request.FILES:
#             file = request.FILES['file']
#             try:
#                 if file.name.endswith('.xls') or file.name.endswith('.xlsx'):
#                     df = pd.read_excel(file)
#                 else:
#                     raise ValueError("Unsupported file format. Only XLS and XLSX files are allowed.")

#                 headers = [header.strip() for header in df.columns]
#                 field_map_normalized = {key.lower().replace(" ", "_"): value for key, value in field_map.items()}
#                 filtered_headers = [header for header in headers if header.lower() in field_map_normalized.values()]

#                 additional_headers = [header for header in headers if header.lower() not in field_map_normalized.values()]
#                 filtered_headers_lower = [header.lower() for header in filtered_headers]
#                 filtered_field_map = {key: value for key, value in field_map.items() if value in filtered_headers_lower}

#                 df_dict = df.to_dict(orient='records')
#                 json_data = json.dumps(df_dict, default=date_handler)
#                 request.session['df'] = json_data
#                 request.session['field_map'] = field_map

#                 context = {'headers': headers, 'field_map': field_map, 'additional_headers': additional_headers}
#                 return render(request, 'multi_company/mapping_dossier_modal.html', context)
#             except Exception as e:
#                 messages.error(request, f'Error reading file: {str(e)}')
#                 return redirect('doisser')

#         elif 'mapping' in request.POST:
#             mapping_data = {}
#             custom_fields = {}

#             for field, field_name in field_map.items():
#                 mapping_data[field] = request.POST.get(field, '')

#             for custom_field in request.POST.getlist('custom_fields'):
#                 custom_fields[custom_field] = custom_field

#             mapping_data.update({'custom_fields': custom_fields})

#             df_records = request.session.get('df', [])
#             field_map = request.session.get('field_map', {})

#             leads = []
#             for record in json.loads(df_records):
#                 lead_data = {}
#                 for header, field in mapping_data.items():
#                     if field == '__empty__':
#                         value_holder = None
#                     elif header == 'custom_fields':
#                         custom_f = {}
#                         for excess_key, excess_fields in field.items():
#                             excess_value = record.get(excess_key)
#                             excess_value_holder = None
#                             if (isinstance(excess_value, float) and math.isnan(excess_value)) or excess_value == 'NaT':
#                                 excess_value_holder = ''
#                             else:
#                                 excess_value_holder =  excess_value
#                             custom_f[excess_key] = excess_value_holder
#                         lead_data['custom_fields'] = custom_f
#                     else:
#                         value = record.get(field)
#                         value_holder = None
#                         if header.startswith('date_'):
#                             date_value = parse_date(value)
#                             value_holder = date_value if not pd.isna(date_value) else None
#                         elif isinstance(value, float) and math.isnan(value):
#                             value_holder = ''
#                         elif isinstance(value, float) and not math.isnan(value):
#                             value_holder = int(value) if value.is_integer() else value
#                         else:
#                             value_holder = record[field]

#                         lead_data[header] = value_holder

#                 leads.append(Doisser(**lead_data))

#             Doisser.objects.bulk_create(leads)
#             request.session.pop('df', None)
#             request.session.pop('field_map', None)

#             messages.success(request, f'{len(leads)} leads imported successfully.')

#             return redirect('doisser')

#     return redirect('doisser')






