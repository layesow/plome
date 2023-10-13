# multi_company/models.py

from django.db import models





class Formation(models.Model):
    date_de_soumission = models.DateField(null=True, blank=True)
    nom_de_la_campagne = models.CharField(max_length=100, null=True, blank=True)
    nom_prenom = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    conseiller = models.CharField(max_length=100, null=True, blank=True)
    custom_fields = models.JSONField(blank=True, null=True)
    company = models.ForeignKey('leads.Company', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom_prenom  # You can change this to represent the model as needed

from django.db import models


class FormSettings(models.Model):
    company = models.ForeignKey('leads.Company', on_delete=models.CASCADE)
    form_name = models.CharField(max_length=100)

    def __str__(self):
        return self.form_name


    
class Doisser(models.Model):   
    date_dinscription = models.DateField(null=True, blank=True)
    numero_edof = models.CharField(max_length=100,null=True, blank=True)
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.BigIntegerField(null=True, blank=True)
    mail = models.CharField(max_length=250, null=True, blank=True)
    address_postal = models.CharField(max_length=300, null=True, blank=True)
    statut_edof = models.CharField(max_length=100, null=True, blank=True)
    challenge = models.CharField(max_length=300, null=True, blank=True)
    colis_a_preparer = models.CharField(max_length=300, null=True, blank=True)
    prix_net = models.BigIntegerField(null=True, blank=True)
    conseiller = models.CharField(max_length=100, null=True, blank=True)
    equipes = models.CharField(max_length=100, null=True, blank=True)
    criteres_com = models.BigIntegerField(null=True, blank=True)
    
    date_prevue_d_entree_en_formation = models.DateTimeField(null=True, blank=True)
    date_prevue_de_fin_de_formation = models.DateTimeField(null=True, blank=True)
     
    history = models.ForeignKey(
        'leads.LeadHistory',  # Use the string format to avoid circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doissers'
    )
    appel_effectue_le_date_time = models.DateTimeField(null=True, blank=True)
    appel_effectue_le_motifs = models.DateTimeField(null=True, blank=True)
    
 
    rdv_confirme_dateandtime = models.DateTimeField(null=True, blank=True)
    rdv_confirme_confirmateur = models.CharField(max_length=100, null=True, blank=True)
    rdv_confirme_statut_service_confirmateur = models.CharField(max_length=100, null=True, blank=True)
    
   
    inscription_visio_entree_audio = models.BooleanField(null=True, blank=True)
    inscription_visio_entree_niveau_de_relance = models.CharField(max_length=100, null=True, blank=True)
    inscription_visio_entree_somme_facturee = models.IntegerField(null=True, blank=True)
    inscription_visio_entree_date_de_facturation = models.DateTimeField(null=True, blank=True)
    inscription_visio_entree_date_d_encaissement = models.DateTimeField(null=True, blank=True)
    inscription_visio_entree_facture = models.BooleanField(null=True, blank=True)
    inscription_visio_entree_num_facture = models.CharField(max_length=300 ,null=True, blank=True)
    inscription_visio_entree_colis_a_envoyer_le = models.DateTimeField(null=True, blank=True)
    inscription_visio_entree_numero_de_suivi_vers_point_relais = models.CharField(max_length=100, null=True, blank=True)
    inscription_visio_entree_commentaires = models.CharField(max_length=300, null=True, blank=True)
    inscription_visio_entree_statut_colis = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey('leads.Company', on_delete=models.SET_NULL, null=True, blank=True)
    custom_fields = models.JSONField(null=True, blank=True)

    def _str_(self):
        return self.prenom



class JotFormSubmission(models.Model):
    submission_date = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    numero_telephone = models.CharField(max_length=255, null=True, blank=True)
    numero_et_rue = models.CharField(max_length=255, null=True, blank=True)
    complement_adresse = models.CharField(max_length=255, null=True, blank=True)
    ville = models.CharField(max_length=255, null=True, blank=True)
    etat_region = models.CharField(max_length=255, null=True, blank=True)
    code_postal = models.CharField(max_length=255, null=True, blank=True)
    choix_formation = models.CharField(max_length=255, null=True, blank=True)
    date_debut = models.CharField(max_length=255, null=True, blank=True)
    date_fin = models.CharField(max_length=255, null=True, blank=True)
    nombre_heure = models.CharField(max_length=255, null=True, blank=True)
    prix_formation = models.CharField(max_length=255, null=True, blank=True)
    passage_au = models.CharField(max_length=255, null=True, blank=True)
    votre_conseiller = models.CharField(max_length=255, null=True, blank=True)
    formation = models.CharField(max_length=255, null=True, blank=True)
    audio_appel_qualite = models.CharField(max_length=255, null=True, blank=True)
    audio_suivi_formation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.first_name



