from django.contrib import admin
from import_export.admin import ImportExportModelAdmin # Assicurati che sia questo
from .models import Articolo
from .resources import ArticoloResource # Importa la tua risorsa personalizzata

@admin.register(Articolo)
class ArticoloAdmin(ImportExportModelAdmin): # Eredita da ImportExportModelAdmin
    resource_class = ArticoloResource # Usa la tua risorsa
    list_display = (
        'numero_sequenziale',
        'codice_articolo',
        'descrizione',
        'um',
        'data_conferimento', # Ora puoi mostrarla
        'attivo',
        'conta_arrivi',
    )
    list_filter = (
        'attivo',
        'data_conferimento', # Ora puoi filtrare per data
        'codice_articolo',
    )
    search_fields = (
        'codice_articolo',
        'descrizione',
        'codice_fornitore',
        'partita_produzione',
    )
    ordering = ('-data_conferimento', '-numero_sequenziale',)
    # Aggiungi campi readonly se necessario, es. numero_sequenziale e conta_arrivi
    readonly_fields = ('numero_sequenziale', 'conta_arrivi')