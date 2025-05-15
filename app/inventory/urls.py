from django.urls import path
from . import views 

app_name = 'inventory'

urlpatterns = [
    path('', views.ArticoloListView.as_view(), name='lista'),
    path('articolo/add/', views.ArticoloCreateView.as_view(), name='new'),
    path('articolo/<int:pk>/edit/', views.ArticoloUpdateView.as_view(), name='edit'),

    # Flusso di importazione a più passaggi
    path('import/upload/', views.upload_file_view, name='upload_file'), # Vecchia 'articolo-import' ora è 'upload_file'
    path('import/map/', views.map_columns_view, name='map_columns'),
    path('import/process/', views.process_import_view, name='process_import'),
    
    path('export/', views.export_articoli, name='articolo-export'),
]