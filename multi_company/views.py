from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
import pandas as pd
from .models import Doisser
from django.contrib import messages
import datetime
from leads.models import Company 






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






