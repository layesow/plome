# # multi_company/views.py
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from accounts.models import CustomUserTypes
from django.shortcuts import render, redirect, get_object_or_404
# from .models import User

from django.shortcuts import render
from .models import Company  # Import the Company model
def company_dropdown_view(request):
    companies = Company.objects.all()
    return {'companies': companies}

    

def doisser(request):
    return render(request,'multi_company/doisser.html')



# multi_company/views.py
import json
import math
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Doisser

from datetime import datetime

def parse_date(date_str):
    # Define different date formats that may appear in the CSV
    date_formats = ["%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M", "%d-%m-%Y %H:%M", "%d/%m/%Y"]

    # Try parsing the date using each format until one succeeds or return None if all fail
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(str(date_str), date_format)
            # Format the parsed date as '%Y-%m-%d %H:%M:%S'
            formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
            return formatted_date
        except ValueError:
            continue
    return None



import pandas as pd
from .models import Doisser
from django.contrib import messages
from datetime import datetime

from datetime import datetime


from datetime import datetime

def parse_date(date_str):
    # Define different date formats that may appear in the CSV
    date_formats = [
        "%Y-%m-%d %H:%M:%S",   # Example: "2023-01-08 00:00:00"
        "%m/%d/%Y %H:%M",      # Example: "1/8/2023 00:00"
        "%d/%m/%Y",            # Example: "1/8/2023" or "08/01/2023"
        "%d-%m-%Y %H:%M",      # Example: "08-01-2023 00:00"
        "%Y-%m-%d",            # Example: "2023-01-08"
        "%m/%d/%Y",            # Example: "1/8/2023" or "08/01/2023"
        "%d/%m/%y",            # Example: "1/8/23" or "08/01/23"
        "%d-%m-%y",            # Example: "08-01-23"
        "%d.%m.%Y",            # Example: "08.01.2023"
        "%d.%m.%y",            # Example: "08.01.23"
        "%b %d, %Y",           # Example: "Jan 8, 2023"
        "%b %d %Y",            # Example: "Jan 8 2023"
    ]

    # Try parsing the date using each format until one succeeds or return None if all fail
    for date_format in date_formats:
        try:
            return datetime.strptime(str(date_str), date_format)
        except ValueError:
            continue
    return None



def doisser(request):
    records = Doisser.objects.all()  # Fetch all Doisser records from the database
    return render(request, 'multi_company/doisser.html', {'records': records})

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
            # "AG :" : "inscription_visio_entree_colis_a_envoyer_le",
            "AI" : "inscription_visio_entree_numero_de_suivi_vers_point_relais",
            "AJ" : "inscription_visio_entree_commentaires",
            "AH" : "inscription_visio_entree_statut_colis",
        }
  
        df.rename(columns=column_mapping, inplace=True)
        df.fillna("", inplace=True)
        
        for _, row in df.iterrows():
            # date_dinscription = datetime.strptime(str(row['date_dinscription']), "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            # date_dinscription = datetime.strptime(str(row['date_dinscription']), "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")


           # date_dinscription = datetime.strptime(row['date_dinscription'], "%d-%m-%Y").strftime("%Y-%m-%d")
            date_dinscription = parse_date(row['date_dinscription'])
            numero_edof=row['numero_edof'] if row['numero_edof'] else None
            nom=row['nom'] 
            prenom=row['prenom']
            # telephone=row['telephone']
            telephone = int(row['telephone']) if row['telephone'].isdigit() else None if row['telephone'] else None

            mail=row['mail']
            address_postal=row['address_postal'] if row['address_postal'] else None
            statut_edof=row['statut_edof'] if row['address_postal'] else None
            challenge=row['challenge'] if row['address_postal'] else None
            colis_a_preparer=row['colis_a_preparer'] if row['colis_a_preparer'] else None
            prix_net=row['prix_net'] if row['prix_net'] else None 
            conseiller=row['conseiller'] if row['conseiller'] else None
            equipes=row['equipes'] if row['equipes'] else None
            criteres_com=row['criteres_com'] if row['criteres_com'] else None
            date_prevue_d_entree_en_formation = parse_date(row['date_prevue_d_entree_en_formation'])
          
            date_prevue_de_fin_de_formation = parse_date(row['date_prevue_de_fin_de_formation'])
            # appel_effectue_le_date_time=datetime.strptime(row['appel_effectue_le_date_time'], "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            #appel_effectue_le_date_time = datetime.strptime(row['appel_effectue_le_date_time'], "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S") if row['appel_effectue_le_date_time'] else None
            appel_effectue_le_date_time = parse_date(row['appel_effectue_le_date_time'])
            appel_effectue_le_motifs=datetime.strptime(row['appel_effectue_le_motifs'], "%d-%m-%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S") if row['appel_effectue_le_motifs'] else None
            #rdv_confirme_dateandtime=datetime.strptime(row['rdv_confirme_dateandtime'], "%d-%m-%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S") if row['rdv_confirme_dateandtime'] else None
            rdv_confirme_dateandtime = parse_date(row['rdv_confirme_dateandtime'])
            rdv_confirme_confirmateur=row['rdv_confirme_confirmateur'] if row['rdv_confirme_confirmateur'] else None
            rdv_confirme_statut_service_confirmateur=row['rdv_confirme_statut_service_confirmateur']  if row['rdv_confirme_statut_service_confirmateur'] else None
            inscription_visio_entree_audio=row['inscription_visio_entree_audio']
            inscription_visio_entree_niveau_de_relance=row['inscription_visio_entree_niveau_de_relance']
            inscription_visio_entree_somme_facturee=row['inscription_visio_entree_somme_facturee'] if row['inscription_visio_entree_somme_facturee'] else None 
            inscription_visio_entree_date_de_facturation = parse_date(row['inscription_visio_entree_date_de_facturation'])
           # inscription_visio_entree_date_de_facturation=datetime.strptime(row['inscription_visio_entree_date_de_facturation'], "%d-%m-%Y").strftime("%Y-%m-%d %H:%M:%S") if row['inscription_visio_entree_date_de_facturation'] else None
            inscription_visio_entree_date_d_encaissement = parse_date(row['inscription_visio_entree_date_d_encaissement'])
           # inscription_visio_entree_date_d_encaissement=datetime.strptime(row['inscription_visio_entree_date_d_encaissement'], "%d-%m-%Y").strftime("%Y-%m-%d %H:%M:%S") if row['inscription_visio_entree_date_d_encaissement'] else None
            inscription_visio_entree_facture=row['inscription_visio_entree_facture']  if row['inscription_visio_entree_facture'] else None
            inscription_visio_entree_num_facture=row['inscription_visio_entree_num_facture']  if row['inscription_visio_entree_num_facture'] else None
            # inscription_visio_entree_colis_a_envoyer_le=datetime.strptime(row['inscription_visio_entree_colis_a_envoyer_le'], "%d-%m-%Y").strftime("%Y-%m-%d %H:%M:%S") if row['inscription_visio_entree_colis_a_envoyer_le'] else None
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
                # inscription_visio_entree_colis_a_envoyer_le = inscription_visio_entree_colis_a_envoyer_le,
                inscription_visio_entree_numero_de_suivi_vers_point_relais = inscription_visio_entree_numero_de_suivi_vers_point_relais,
                inscription_visio_entree_commentaires = inscription_visio_entree_commentaires,
                inscription_visio_entree_statut_colis = inscription_visio_entree_statut_colis
            )
            Doisser_data.save()
            
    return redirect('doisser')

from .models import Doisser
from django.http import JsonResponse
  # Import the parse_date function from your module

def edit_doisser_lead(request, record_id):
    lead = get_object_or_404(Doisser, id=record_id)

    if request.method == 'POST':
        try:
            # Update the Doisser object with the data from the POST request
            lead.date_dinscription = parse_date(request.POST.get('date_dinscription'))
            lead.numero_edof = request.POST.get('numero_edof')
            lead.nom = request.POST.get('nom')
            lead.prenom = request.POST.get('prenom')
            lead.telephone = int(request.POST.get('telephone')) if request.POST.get('telephone').isdigit() else None
            lead.mail = request.POST.get('mail')
            lead.address_postal = request.POST.get('address_postal')
            lead.statut_edof = request.POST.get('statut_edof')
            lead.challenge = request.POST.get('challenge')
            lead.colis_a_preparer = request.POST.get('colis_a_preparer')
            lead.prix_net = request.POST.get('prix_net')
            lead.conseiller = request.POST.get('conseiller')
            lead.equipes = request.POST.get('equipes')
            lead.criteres_com = request.POST.get('criteres_com')
            lead.date_prevue_d_entree_en_formation = parse_date(request.POST.get('date_prevue_d_entree_en_formation'))
            lead.date_prevue_de_fin_de_formation = parse_date(request.POST.get('date_prevue_de_fin_de_formation'))
            lead.appel_effectue_le_date_time = parse_date(request.POST.get('appel_effectue_le_date_time'))
            lead.appel_effectue_le_motifs = parse_date(request.POST.get('appel_effectue_le_motifs'))
            lead.rdv_confirme_dateandtime = parse_date(request.POST.get('rdv_confirme_dateandtime'))
            lead.rdv_confirme_confirmateur = request.POST.get('rdv_confirme_confirmateur')
            lead.rdv_confirme_statut_service_confirmateur = request.POST.get('rdv_confirme_statut_service_confirmateur')
            lead.inscription_visio_entree_audio = request.POST.get('inscription_visio_entree_audio')
            lead.inscription_visio_entree_niveau_de_relance = request.POST.get('inscription_visio_entree_niveau_de_relance')
            lead.inscription_visio_entree_somme_facturee = request.POST.get('inscription_visio_entree_somme_facturee')
            lead.inscription_visio_entree_date_de_facturation = parse_date(request.POST.get('inscription_visio_entree_date_de_facturation'))
            lead.inscription_visio_entree_date_d_encaissement = parse_date(request.POST.get('inscription_visio_entree_date_d_encaissement'))
            lead.inscription_visio_entree_facture = request.POST.get('inscription_visio_entree_facture')
            lead.inscription_visio_entree_num_facture = request.POST.get('inscription_visio_entree_num_facture')
            lead.inscription_visio_entree_numero_de_suivi_vers_point_relais = request.POST.get('inscription_visio_entree_numero_de_suivi_vers_point_relais')
            lead.inscription_visio_entree_commentaires = request.POST.get('inscription_visio_entree_commentaires')
            lead.inscription_visio_entree_statut_colis = request.POST.get('inscription_visio_entree_statut_colis')

            lead.save()  # Save the changes to the Doisser object
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': str(e)})

    return render(request, 'multi_company/doisser.html', {'doisser': lead})



# views.py
# views.py


from django.shortcuts import render, redirect
from .models import Company

def select_company(request):
    if request.method == 'POST':
        selected_company_id = request.POST.get('company')
        if selected_company_id:
            try:
                selected_company = Company.objects.get(pk=selected_company_id)

                # Determine the HTML page to redirect based on the selected company
                if selected_company.name == 'AA':
                    return redirect('admin_dashboard')  # Replace 'admin_dashboard' with the URL name of your admin dashboard view
                # Add more conditions for other companies as needed
                else:
                    return render(request, 'error.html', {'message': 'Invalid Company'})
            except Company.DoesNotExist:
                return render(request, 'error.html', {'message': 'Company not found'})
    
    companies = Company.objects.all()
    return render(request, 'multi_company/company1.html', {'companies': companies})


from .models import Doisser
from django.shortcuts import render, redirect

# Your parse_date function here

def add_doisser_lead(request):
    if request.method == 'POST':
        # Get form data with default value of None for empty fields
        date_dinscription = parse_date(request.POST.get('date_dinscription', None))
        numero_edof = request.POST.get('numero_edof', None)
        nom = request.POST.get('nom', None)
        prenom = request.POST.get('prenom', None)
        telephone = int(request.POST.get('telephone')) if request.POST.get('telephone').isdigit() else None
        mail = request.POST.get('mail', None)
        address_postal = request.POST.get('address_postal', None)
        statut_edof = request.POST.get('statut_edof', None)
        challenge = request.POST.get('challenge', None)
        colis_a_preparer = request.POST.get('colis_a_preparer', None)
        prix_net = request.POST.get('prix_net', None)
        prix_net = float(prix_net) if prix_net and prix_net.strip() else None
        criteres_com = request.POST.get('criteres_com', None)
        criteres_com = float(criteres_com) if criteres_com and criteres_com.strip() else None
        date_prevue_d_entree_en_formation = parse_date(request.POST.get('date_prevue_d_entree_en_formation', None))
        date_prevue_de_fin_de_formation = parse_date(request.POST.get('date_prevue_de_fin_de_formation', None))
        appel_effectue_le_date_time = parse_date(request.POST.get('appel_effectue_le_date_time', None))
        appel_effectue_le_motifs = request.POST.get('appel_effectue_le_motifs', None)
        rdv_confirme_dateandtime = parse_date(request.POST.get('rdv_confirme_dateandtime', None))
        rdv_confirme_confirmateur = request.POST.get('rdv_confirme_confirmateur', None)
        rdv_confirme_statut_service_confirmateur = request.POST.get('rdv_confirme_statut_service_confirmateur', None)
        inscription_visio_entree_audio = request.POST.get('inscription_visio_entree_audio', None)
        inscription_visio_entree_niveau_de_relance = request.POST.get('inscription_visio_entree_niveau_de_relance', None)
        inscription_visio_entree_somme_facturee = request.POST.get('inscription_visio_entree_somme_facturee', None)
        inscription_visio_entree_somme_facturee = float(inscription_visio_entree_somme_facturee) if inscription_visio_entree_somme_facturee and inscription_visio_entree_somme_facturee.strip() else None
        inscription_visio_entree_date_de_facturation = parse_date(request.POST.get('inscription_visio_entree_date_de_facturation', None))
        inscription_visio_entree_date_d_encaissement = parse_date(request.POST.get('inscription_visio_entree_date_d_encaissement', None))
        inscription_visio_entree_facture = request.POST.get('inscription_visio_entree_facture', None)
        inscription_visio_entree_num_facture = request.POST.get('inscription_visio_entree_num_facture', None)
        inscription_visio_entree_numero_de_suivi_vers_point_relais = request.POST.get('inscription_visio_entree_numero_de_suivi_vers_point_relais', None)
        inscription_visio_entree_commentaires = request.POST.get('inscription_visio_entree_commentaires', None)
        inscription_visio_entree_statut_colis = request.POST.get('inscription_visio_entree_statut_colis', None)
        # Handle JSONField separately (assuming it's sent as JSON in the POST request)
        custom_fields = request.POST.get('custom_fields', None)

        # Create a new Doisser Lead record with empty fields
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






