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
    #path('lead_doisser_history_view/<int:lead_id>/', views.doisser_view, name='lead_doisser_history_view'),
  
 
    
  
    
  
]
