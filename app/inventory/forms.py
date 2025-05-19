# EntrataMerci/app/inventory/forms.py
from django import forms
from .models import Articolo, Deposito, Posizione

class ArticoloForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = [ # Elenco esplicito è meglio di '__all__'
            'numero_sequenziale', 'nome_articolo', 'descrizione', 'tipologia_articolo',
            'unita_di_misura', 'prezzo_unitario', 'quantita', 'deposito',
            'posizione', 'attivo', 'codice_fornitore', 'partita_produzione',
            'data_inserimento', # Rimosso 'data_ultima_modifica' perché auto_now=True
        ]
        widgets = {
            'data_inserimento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'descrizione': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se data_inserimento è un campo DateTimeField(default=timezone.now)
        # e vuoi che sia editabile ma con un default nel form:
        if not self.instance.pk and 'data_inserimento' in self.fields:
             # Non impostare initial qui se default=timezone.now è sufficiente
             # self.fields['data_inserimento'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')
             pass
        # Se vuoi che il campo posizione sia filtrato in base al deposito selezionato (richiede JS o approcci più avanzati)
        # Per ora, lo lasciamo standard.


# Form per Deposito
class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = ['nome_deposito', 'indirizzo']
        widgets = {
            'indirizzo': forms.Textarea(attrs={'rows': 3}),
        }

# Form per Posizione
class PosizioneForm(forms.ModelForm):
    class Meta:
        model = Posizione
        fields = ['deposito', 'nome_posizione']
        # Potresti voler personalizzare il widget per 'deposito' se hai molti depositi
        # widgets = {
        #     'deposito': forms.Select(attrs={'class': 'form-select'}),
        # }

# Form per l'upload del file di importazione Articoli
class ArticoloImportForm(forms.Form):
    file = forms.FileField(label="Seleziona file Articoli (.xls, .xlsx, .csv)")

# Potresti aggiungere anche DepositoImportForm e PosizioneImportForm se necessario
# class DepositoImportForm(forms.Form):
#     file = forms.FileField(label="Seleziona file Depositi (.xls, .xlsx, .csv)")

# class PosizioneImportForm(forms.Form):
#     file = forms.FileField(label="Seleziona file Posizioni (.xls, .xlsx, .csv)")