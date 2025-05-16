# EntrataMerci/app/inventory/forms.py
from django import forms
from .models import Articolo, Deposito, Posizione

class ArticoloForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = '__all__' # O specifica i campi
        widgets = { # Esempio per rendere i campi data selezionabili
            'data_inserimento': forms.DateInput(attrs={'type': 'date'}),
            'data_ultima_modifica': forms.DateInput(attrs={'type': 'date'}),
        }

class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = '__all__'

class PosizioneForm(forms.ModelForm):
    class Meta:
        model = Posizione
        fields = '__all__'

# Form per l'upload del file di importazione
class ArticoloImportForm(forms.Form):
    file = forms.FileField(label="Seleziona file (.xls, .xlsx, .csv)")

# Crea ImportForm simili per Deposito e Posizione se hai import per loro
# class DepositoImportForm(forms.Form):
#     file = forms.FileField(label="Seleziona file (.xls, .xlsx, .csv)")