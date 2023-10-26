# multi_company/urls.py
from django.urls import path
from . import views 
#from .views import GeneratePDF


urlpatterns = [
   # path('company_dropdown_view/', views.company_dropdown_view, name='company_dropdown_view'),
    path('doisser/',views.doisser, name='doisser'),
    path('import_doisser_leads/', views.import_doisser_leads, name='import_doisser_leads'),
    path('edit_doisser_lead/<int:pid>/', views.edit_doisser_lead, name='edit_doisser_lead'),
   # path('select_company/', views.select_company, name='select_company'),
    path('add_doisser_lead/', views.add_doisser_lead, name='add_doisser_lead'),
    path('doisser_detail/<int:record_id>/', views.doisser_detail, name='doisser_detail'),
    path('add_formation/', views.add_formation, name='add_formation'),
    path('create_form_settings/', views.create_form_settings, name='create_form_settings'),
    path('import_jotform_data/', views.import_jotform_data, name = "import_jotform_data"),
    path('add_jotform/', views.add_jotform, name='add_jotform'),
    path('import_jotform_data_aa/', views.import_jotform_data_aa, name = "import_jotform_data_aa"),
    path('show_jotform_data/', views.show_jotform_data, name='show_jotform_data'),
    path('save_appointment_doisser/', views.save_appointment, name='save_appointment_doisser'),
    path('map_jotform_to_doisser/', views.map_jotform_to_doisser, name='map_jotform_to_doisser'),
    # path('edit_formation/<int:formation_id>/', views.edit_formation, name='edit_formation'),
  
 
    
  
    
  
]
