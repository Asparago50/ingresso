# EntrataMerci/app/inventory/urls.py
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home_inventory, name='home_inventory'),

    # URL per Articolo
    path('articoli/', views.ArticoloListView.as_view(), name='articolo_list'),
    path('articoli/create/', views.ArticoloCreateView.as_view(), name='articolo_create'),
    path('articoli/<int:pk>/update/', views.ArticoloUpdateView.as_view(), name='articolo_update'),
    path('articoli/<int:pk>/delete/', views.ArticoloDeleteView.as_view(), name='articolo_delete'),
    path('articoli/import/', views.import_articoli, name='articolo_import'),
    path('articoli/export/', views.export_articoli, name='articolo_export'),

    # URL per Deposito
    path('depositi/', views.DepositoListView.as_view(), name='deposito_list'),
    path('depositi/create/', views.DepositoCreateView.as_view(), name='deposito_create'),
    path('depositi/<int:pk>/update/', views.DepositoUpdateView.as_view(), name='deposito_update'),
    path('depositi/<int:pk>/delete/', views.DepositoDeleteView.as_view(), name='deposito_delete'),
    # Aggiungi URL per import/export depositi se li implementi

    # URL per Posizione
    path('posizioni/', views.PosizioneListView.as_view(), name='posizione_list'),
    path('posizioni/create/', views.PosizioneCreateView.as_view(), name='posizione_create'),
    path('posizioni/<int:pk>/update/', views.PosizioneUpdateView.as_view(), name='posizione_update'),
    path('posizioni/<int:pk>/delete/', views.PosizioneDeleteView.as_view(), name='posizione_delete'),
    # Aggiungi URL per import/export posizioni se li implementi
]