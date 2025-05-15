from django import forms
from .models import Articolo

class ArticoloForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = [
            'codice_articolo', 'trasposizione', 'descrizione', 'um',
            'pezzatura', 'giacenza', 'codice_fornitore',
            'anagrafica_fornitore', 'scheda_riferimento',
            # 'data_conferimento', # RIMOSSO perché auto_now_add=True nel modello
            'partita_produzione',
            'quantita_conferita', 'attivo'
        ]
        widgets = {
            'descrizione': forms.Textarea(attrs={'rows': 3}),
            'anagrafica_fornitore': forms.Textarea(attrs={'rows': 3}),
            # 'data_conferimento': forms.DateInput(attrs={'type': 'date'}), # Rimosso perché il campo è rimosso
        }

    def clean_codice_articolo(self):
        val = self.cleaned_data.get('codice_articolo', '').strip() # Usa .get per sicurezza
        if not val:
             raise forms.ValidationError("Il Codice Articolo è obbligatorio.")
        # Esempio: if ' ' in val:
        #    raise forms.ValidationError("Non sono permessi spazi in Codice Articolo")
        return val

class ArticoloImportForm(forms.Form):
    file_upload = forms.FileField(
        label='Seleziona file da importare (CSV, Excel)',
        required=True,
        help_text='Assicurati che il file abbia le colonne corrette.'
    )
