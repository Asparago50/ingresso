# EntrataMerci/app/inventory/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView # Aggiunto DetailView se lo usi
from django.http import HttpResponse # Per export_data se restituisce direttamente

# --- IMPORT PER AUTENTICAZIONE E PERMESSI ---
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required # <<< ASSICURATI CHE CI SIA QUESTA RIGA COMPLETA

# --- I tuoi modelli e form ---
from .models import Articolo, Deposito, Posizione # Importa tutti i modelli che gestisci con le viste
from .forms import (
    ArticoloForm, DepositoForm, PosizioneForm,
    ArticoloImportForm, # Assumendo che tu abbia form di import specifici
    # Altri form se necessario
)
from .resources import ArticoloResource # Per django-import-export

# Helper per django-import-export (se usi la vista custom come nel tuo codice)
from tablib import Dataset
from django.contrib import messages

# Esempio Viste per ARTICOLO
# ===========================

class ArticoloListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Articolo
    template_name = 'inventory/list.html' # Assicurati che esista o adatta al tuo 'inventory/articolo_list.html'
    context_object_name = 'articoli'
    permission_required = 'inventory.view_articolo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Articolo'
        context['model_name_plural'] = 'Articoli'
        context['create_url_name'] = 'inventory:articolo_create' # Aggiungi questo
        return context

class ArticoloCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Articolo
    form_class = ArticoloForm
    template_name = 'inventory/form.html' # Assicurati che esista o adatta al tuo 'inventory/articolo_form.html'
    success_url = reverse_lazy('inventory:articolo_list')
    permission_required = 'inventory.add_articolo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Crea Nuovo Articolo'
        return context

class ArticoloUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Articolo
    form_class = ArticoloForm
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('inventory:articolo_list')
    permission_required = 'inventory.change_articolo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Modifica Articolo: {self.object.nome_articolo}' # Adatta al campo nome
        return context

class ArticoloDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Articolo
    template_name = 'inventory/confirm_delete.html' # Crea questo template
    success_url = reverse_lazy('inventory:articolo_list')
    permission_required = 'inventory.delete_articolo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_to_delete'] = self.object
        return context

# Dovrai creare viste simili (ListView, CreateView, UpdateView, DeleteView)
# per i modelli DEPOSITO e POSIZIONE, ognuna con i permessi appropriati:
# Esempio per DepositoListView:
# class DepositoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = Deposito
#     permission_required = 'inventory.view_deposito'
#     # ... etc ...

# Viste per IMPORT/EXPORT
# =======================
# La tua vista import_articoli sembra corretta con django-import-export,
# dobbiamo solo aggiungere i decoratori.

@login_required
@permission_required('inventory.add_articolo', raise_exception=True) # O 'inventory.change_articolo' se l'import può aggiornare
def import_articoli(request): # Rinominata per chiarezza, prima era import_data
    if request.method == 'POST':
        form = ArticoloImportForm(request.POST, request.FILES)
        if form.is_valid():
            articolo_resource = ArticoloResource()
            dataset = Dataset()
            try:
                new_articoli = request.FILES['file']
                # Controlla l'estensione del file
                if not new_articoli.name.endswith(('.xls', '.xlsx', '.csv')):
                    messages.error(request, 'Formato file non supportato. Usa .xls, .xlsx o .csv')
                    return render(request, 'inventory/form_import.html', {'form': form, 'model_name_plural': 'Articoli'})

                if new_articoli.name.endswith('.csv'):
                    imported_data = dataset.load(new_articoli.read().decode('utf-8'), format='csv')
                else: # Assume .xls o .xlsx
                    imported_data = dataset.load(new_articoli.read(), format='xlsx')

                # Qui puoi mappare le colonne se necessario, come nel tuo codice originale
                # Esempio base (assicurati che i nomi delle colonne nel file corrispondano ai campi del modello):
                # result = articolo_resource.import_data(dataset, dry_run=True, collect_failed_rows=True)

                # Mappatura colonne come nel tuo esempio precedente:
                column_map = {
                    'Numero Sequenziale': 'numero_sequenziale',
                    'Nome Articolo': 'nome_articolo',
                    'Descrizione': 'descrizione',
                    'Tipologia Articolo': 'tipologia_articolo',
                    'Unità di Misura': 'unita_di_misura',
                    'Prezzo Unitario': 'prezzo_unitario',
                    'Quantità': 'quantita',
                    'Data di Inserimento': 'data_inserimento',
                    'Data Ultima Modifica': 'data_ultima_modifica',
                    'Deposito': 'deposito',
                    'Posizione': 'posizione',
                }
                # Ricrea il dataset con gli header corretti per il modello
                mapped_dataset = Dataset()
                mapped_dataset.headers = [column_map.get(h, h) for h in imported_data.headers] # Mappa gli header
                for row in imported_data:
                    mapped_dataset.append(row)

                result = articolo_resource.import_data(mapped_dataset, dry_run=True, collect_failed_rows=True)


                if not result.has_errors() and not result.has_validation_errors():
                    articolo_resource.import_data(mapped_dataset, dry_run=False)
                    messages.success(request, 'Dati importati con successo!')
                    return redirect('inventory:articolo_list') # O dove vuoi reindirizzare
                else:
                    # Gestisci errori e righe fallite
                    error_html = "Errori durante l'importazione:<br>"
                    if result.has_errors():
                        for error in result.base_errors:
                            error_html += f"Errore generale: {error.error}<br>"
                        for row_num, row_errors in result.row_errors():
                            for error in row_errors:
                                error_html += f"Riga {row_num + 1}: Campo '{error.field_name}' - {error.error_message}<br>"

                    if result.has_validation_errors():
                         for invalid_row in result.invalid_rows:
                            error_html += f"Riga {invalid_row.number +1 } ({invalid_row.error_dict}): {invalid_row.error_message}<br>"
                    
                    messages.error(request, error_html, extra_tags='safe')

            except Exception as e:
                messages.error(request, f"Si è verificato un errore imprevisto: {e}")
    else:
        form = ArticoloImportForm()
    return render(request, 'inventory/form_import.html', {
        'form': form,
        'model_name_plural': 'Articoli',
        'page_title': 'Importa Articoli'
    })


@login_required
@permission_required('inventory.view_articolo', raise_exception=True) # Solo chi può vedere può esportare
def export_articoli(request): # Rinominata per chiarezza
    articolo_resource = ArticoloResource()
    dataset = articolo_resource.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="articoli.xlsx"'
    return response

# Se hai import/export per Deposito e Posizione, crea viste simili
# (es. import_depositi, export_depositi) con i permessi corretti.

# La tua vista home, se la mantieni:
@login_required # Tutti devono essere loggati per vedere la home
def home_inventory(request): # Rinominata per evitare conflitti con 'home' di Django
    # ... logica per la tua home dell'inventario ...
    # Ad esempio, mostrare gli ultimi articoli o statistiche
    ultimi_articoli = Articolo.objects.order_by('-data_ultima_modifica')[:5]
    numero_articoli = Articolo.objects.count()
    numero_depositi = Deposito.objects.count()

    context = {
        'ultimi_articoli': ultimi_articoli,
        'numero_articoli': numero_articoli,
        'numero_depositi': numero_depositi,
        'page_title': 'Dashboard Inventario'
    }
    return render(request, 'inventory/home_inventory.html', context) # Crea questo template