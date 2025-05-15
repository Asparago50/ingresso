from import_export import resources, fields
from import_export.widgets import BooleanWidget, DecimalWidget, DateWidget
from .models import Articolo
from datetime import datetime, timedelta

# Funzione per convertire la data seriale di Excel in datetime
def excel_date_to_datetime(excel_date_serial):
    if isinstance(excel_date_serial, (int, float)):
        return datetime(1899, 12, 30) + timedelta(days=excel_date_serial)
    # Prova a parsare se è già una stringa data, altrimenti None
    try:
        return datetime.strptime(str(excel_date_serial), '%Y-%m-%d %H:%M:%S') # O altro formato se stringa
    except ValueError:
        try:
            return datetime.strptime(str(excel_date_serial), '%d/%m/%Y')
        except ValueError:
            return None


class CustomDateWidget(DateWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        # Prova a convertire da seriale Excel se è un numero
        if isinstance(value, (int, float)):
            cleaned_value = excel_date_to_datetime(value)
            if cleaned_value:
                return cleaned_value.date() # Restituisce solo la parte data
            else: # Se la conversione fallisce, prova il parsing standard
                return super().clean(str(value), row, *args, **kwargs) # Fallback
        return super().clean(value, row, *args, **kwargs)


class ArticoloResource(resources.ModelResource):
    codice_articolo = fields.Field(column_name='codice articolo', attribute='codice_articolo')
    trasposizione = fields.Field(column_name='Trasposizione', attribute='trasposizione', default='')
    descrizione = fields.Field(column_name='Descrizione', attribute='descrizione')
    um = fields.Field(column_name='UM', attribute='um')
    pezzatura = fields.Field(column_name='Pezzatura', attribute='pezzatura', widget=DecimalWidget())
    giacenza = fields.Field(column_name='giacenza', attribute='giacenza', widget=DecimalWidget())
    codice_fornitore = fields.Field(column_name='Codice Fornitore', attribute='codice_fornitore')
    anagrafica_fornitore = fields.Field(column_name='Anagrafica Fornitore', attribute='anagrafica_fornitore')
    scheda_riferimento = fields.Field(column_name='Scheda Riferimento', attribute='scheda_riferimento')
    
    # Usa il widget personalizzato per la data
    data_conferimento = fields.Field(column_name='Data', attribute='data_conferimento', widget=CustomDateWidget(format='%d/%m/%Y'))
    
    partita_produzione = fields.Field(column_name='PP', attribute='partita_produzione')
    quantita_conferita = fields.Field(column_name='Q.Tà', attribute='quantita_conferita', widget=DecimalWidget())
    attivo = fields.Field(column_name='Attivo', attribute='attivo', widget=BooleanWidget())

    class Meta:
        model = Articolo
        fields = (
            'codice_articolo', 'trasposizione', 'descrizione', 'um',
            'pezzatura', 'giacenza', 'codice_fornitore', 'anagrafica_fornitore',
            'scheda_riferimento', 'data_conferimento', 'partita_produzione',
            'quantita_conferita', 'attivo',
        )
        # Se vuoi che ogni riga importata sia un NUOVO articolo, ometti import_id_fields
        # Se invece vuoi AGGIORNARE articoli esistenti basati su un ID, definisci import_id_fields
        # Ad esempio, se una combinazione di codice_articolo e partita_produzione è unica:
        # import_id_fields = ('codice_articolo', 'partita_produzione')
        # Se vuoi solo creare nuovi record ad ogni importazione:
        # (non definire import_id_fields o lascialo vuoto)

        skip_unchanged = True
        report_skipped = True
        # Non usare `use_transactions` se la logica in `Articolo.save()` fa query che verrebbero committate
        # troppo presto all'interno di una transazione gestita da import-export.
        # Meglio gestire le transazioni a livello di vista se `save()` è complesso.
        # use_transactions = True