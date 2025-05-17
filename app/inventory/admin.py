# EntrataMerci/app/inventory/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Articolo, Deposito, Posizione # Importa anche Deposito e Posizione
from .resources import ArticoloResource

@admin.register(Articolo)
class ArticoloAdmin(ImportExportModelAdmin):
    resource_class = ArticoloResource
    list_display = (
        'numero_sequenziale', # Era 'codice_articolo', ora usiamo il campo esistente
        'nome_articolo',      # Aggiungiamo il nome per chiarezza
        'descrizione',
        'unita_di_misura',    # Era 'um'
        'data_inserimento',   # Era 'data_conferimento'
        'attivo',             # Ora esiste nel modello
        'get_numero_arrivi',  # Metodo custom per 'conta_arrivi'
        'deposito',           # Mostra il deposito collegato
        'posizione',          # Mostra la posizione collegata
    )
    list_filter = (
        'attivo',             # Ora esiste
        'data_inserimento',   # Era 'data_conferimento'
        'tipologia_articolo', # Esempio di filtro su un campo esistente
        'deposito',           # Filtra per deposito (ForeignKey)
    )
    search_fields = (
        'numero_sequenziale', # Era 'codice_articolo'
        'nome_articolo',
        'descrizione',
        'codice_fornitore',   # Ora esiste (se aggiunto)
        'partita_produzione', # Ora esiste (se aggiunto)
    )
    ordering = ('-data_inserimento', 'numero_sequenziale',) # Era '-data_conferimento'
    
    # readonly_fields devono riferirsi a campi o metodi esistenti
    readonly_fields = ('data_ultima_modifica', 'get_numero_arrivi') # 'numero_sequenziale' di solito non è readonly a meno che non sia autogenerato in modo speciale

    fieldsets = (
        (None, {
            'fields': ('numero_sequenziale', 'nome_articolo', 'attivo')
        }),
        ('Dettagli Articolo', {
            'fields': ('descrizione', 'tipologia_articolo', 'unita_di_misura', 'prezzo_unitario', 'quantita')
        }),
        ('Localizzazione', {
            'fields': ('deposito', 'posizione')
        }),
        ('Tracciabilità e Date', {
            'fields': ('codice_fornitore', 'partita_produzione', 'data_inserimento', 'data_ultima_modifica', 'get_numero_arrivi')
        }),
    )

    # Metodo custom per 'conta_arrivi'
    def get_numero_arrivi(self, obj):
        # Qui dovresti implementare la logica per contare gli arrivi.
        # Se hai un modello 'Arrivo' con una ForeignKey ad 'Articolo':
        # return obj.arrivo_set.count() # o il related_name che hai definito
        return "N/D" # Placeholder finché non hai la logica
    get_numero_arrivi.short_description = 'Numero Arrivi'


# Registra anche Deposito e Posizione per poterli gestire dall'admin
@admin.register(Deposito)
class DepositoAdmin(ImportExportModelAdmin): # Puoi usare ImportExport anche qui se vuoi
    list_display = ('nome_deposito', 'indirizzo')
    search_fields = ('nome_deposito',)

@admin.register(Posizione)
class PosizioneAdmin(ImportExportModelAdmin):
    list_display = ('nome_posizione', 'deposito')
    list_filter = ('deposito',)
    search_fields = ('nome_posizione',)