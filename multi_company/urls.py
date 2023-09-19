# multi_company/urls.py
from django.urls import path
from . import views 
#from .views import GeneratePDF


urlpatterns = [
    path('company_dropdown_view/', views.company_dropdown_view, name='company_dropdown_view'),
    path('doisser/',views.doisser, name='doisser'),
    path('import_doisser_leads/', views.import_doisser_leads, name='import_doisser_leads'),
    path('edit_doisser_lead/<int:record_id>/', views.edit_doisser_lead, name='edit_doisser_lead'),
    path('select_company/', views.select_company, name='select_company'),
    path('add_doisser_lead/', views.add_doisser_lead, name='add_doisser_lead'),
  
    
  
]
