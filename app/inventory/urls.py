# EntrataMerci/app/inventory/urls.py
from django.urls import path
from . import views

app_name = 'inventory' # <<<< NECESSARIO per il namespacing (es. 'inventory:articolo_list')

urlpatterns = [
    path('', views.home_inventory, name='home_inventory'), # Home page dell'inventario

    # URL per Articolo
    path('articoli/', views.ArticoloListView.as_view(), name='articolo_list'),
    path('articoli/create/', views.ArticoloCreateView.as_view(), name='articolo_create'),
    path('articoli/<int:pk>/update/', views.ArticoloUpdateView.as_view(), name='articolo_update'),
    path('articoli/<int:pk>/delete/', views.ArticoloDeleteView.as_view(), name='articolo_delete'),
    path('articoli/import/', views.import_articoli, name='articolo_import'),
    path('articoli/export/', views.export_articoli, name='articolo_export'),

    # Aggiungi qui URL simili per Deposito:
    # path('depositi/', views.DepositoListView.as_view(), name='deposito_list'),
    # path('depositi/create/', views.DepositoCreateView.as_view(), name='deposito_create'),
    # ... e così via per update, delete, import, export

    # Aggiungi qui URL simili per Posizione:
    # path('posizioni/', views.PosizioneListView.as_view(), name='posizione_list'),
    # ... e così via
]