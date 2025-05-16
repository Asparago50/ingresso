# EntrataMerci/app/inventory/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView # Assicurati che ListView sia importato
from django.shortcuts import render, redirect
from django.contrib import messages
# from tablib import Dataset # Se lo usi per import/export, altrimenti non serve qui
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Articolo
from .forms import ArticoloForm, ArticoloImportForm
from .resources import ArticoloResource, excel_date_to_datetime # Assicurati che excel_date_to_datetime sia definita o importata correttamente

# Class-Based Views per CRUD base
# class ArticoloListView(ListView): # <--- QUESTA È LA CLASSE CHE MANCAVA O ERA SBAGLIATA 

class InventoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Articolo
    template_name = 'inventory/list.html'
    context_object_name = 'articoli'
    paginate_by = 20
    ordering = ['-numero_sequenziale']

# class ArticoloCreateView(CreateView):

class InventoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Articolo
    form_class = ArticoloForm
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('inventory:lista')

    def form_valid(self, form):
        messages.success(self.request, "Articolo creato con successo!")
        return super().form_valid(form)

class ArticoloUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Articolo
    form_class = ArticoloForm
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('inventory:lista')

    def form_valid(self, form):
        messages.success(self.request, "Articolo aggiornato con successo!")
        return super().form_valid(form)

# Viste per import/export (come le avevamo definite)
# Esempio per una Function-Based View (come import/export se sono FBV)
@login_required
@permission_required('inventory.add_articolo', raise_exception=True) # O il permesso più appropriat
def upload_file_view(request):
    if request.method == 'POST':
        form = ArticoloImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file_upload']
            
            fs_path = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
            os.makedirs(fs_path, exist_ok=True) # Assicura che la directory esista
            fs = FileSystemStorage(location=fs_path)
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_path = fs.path(filename)

            try:
                if filename.endswith('.xlsx'):
                    df_preview = pd.read_excel(uploaded_file_path, nrows=5)
                elif filename.endswith('.csv'):
                    df_preview = pd.read_csv(uploaded_file_path, nrows=5)
                else:
                    messages.error(request, "Formato file non supportato. Usa .xlsx o .csv.")
                    fs.delete(filename)
                    return redirect('inventory:upload_file')
                
                file_columns = list(df_preview.columns)
                request.session['uploaded_file_path'] = uploaded_file_path
                request.session['file_columns'] = file_columns
                return redirect('inventory:map_columns')

            except Exception as e:
                messages.error(request, f"Errore durante la lettura del file: {e}")
                if fs.exists(filename): # Controlla se il file esiste prima di cancellare
                    fs.delete(filename)
                return redirect('inventory:upload_file')
    else:
        form = ArticoloImportForm()
    return render(request, 'inventory/form_import.html', {'form': form, 'title': 'Passo 1: Carica File per Importazione'})

@login_required
@permission_required('inventory.view_articolo', raise_exception=True) # O il permesso più appropriato
def get_articolo_model_fields(): # Spostata qui o importata se è in utils.py
    # Escludi campi auto-creati, relazioni dirette e campi non editabili come 'conta_arrivi'
    excluded_fields = {'numero_sequenziale', 'id', 'conta_arrivi'} # Aggiungi altri campi da escludere dalla mappatura manuale
    return [
        f.name for f in Articolo._meta.get_fields() 
        if not f.auto_created and not f.is_relation and f.name not in excluded_fields
    ]

@login_required
@permission_required('inventory.view_articolo', raise_exception=True) # O il permesso più appropriato
def map_columns_view(request):
    uploaded_file_path = request.session.get('uploaded_file_path')
    file_columns = request.session.get('file_columns')

    if not uploaded_file_path or not file_columns:
        messages.error(request, "Nessun file caricato o colonne non trovate. Riprova.")
        return redirect('inventory:upload_file')

    model_fields = get_articolo_model_fields()

    if request.method == 'POST':
        mapping = {}
        for model_field in model_fields:
            selected_file_column = request.POST.get(f'map_{model_field}')
            if selected_file_column and selected_file_column != "IGNORE":
                mapping[model_field] = selected_file_column
        
        if not mapping:
            messages.error(request, "Nessuna colonna mappata. Seleziona almeno una mappatura.")
            # Rirenderizza la pagina di mappatura passando di nuovo i contesti
            return render(request, 'inventory/map_columns.html', {
                'file_columns': file_columns,
                'model_fields': model_fields,
                'title': 'Passo 2: Mappa Colonne'
            })

        request.session['column_mapping'] = mapping
        return redirect('inventory:process_import')

    return render(request, 'inventory/map_columns.html', {
        'file_columns': file_columns,
        'model_fields': model_fields,
        'title': 'Passo 2: Mappa Colonne'
    })

@login_required
@permission_required('inventory.view_articolo', raise_exception=True) # O il permesso più appropriato
def process_import_view(request):
    uploaded_file_path = request.session.get('uploaded_file_path')
    mapping = request.session.get('column_mapping')

    if not uploaded_file_path or not mapping:
        messages.error(request, "Dati di importazione mancanti (file o mappatura). Riprova.")
        return redirect('inventory:upload_file')

    try:
        filename = os.path.basename(uploaded_file_path)
        if filename.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file_path)
        elif filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file_path)
        else:
            raise ValueError("Formato file non supportato.")

        articoli_creati = 0
        errori_riga = []

        for index, row_data_series in df.iterrows(): # row è una Series di Pandas
            data_to_save = {}
            valid_row = True
            
            # Applica la mappatura e le conversioni
            for model_field, file_column_name in mapping.items():
                if file_column_name in row_data_series and pd.notna(row_data_series[file_column_name]):
                    val = row_data_series[file_column_name]
                    
                    # Conversioni specifiche per campo
                    if model_field == 'attivo':
                        val_attivo = str(val).strip().upper()
                        if val_attivo in ['SI', 'TRUE', '1', 'T']: data_to_save[model_field] = True
                        elif val_attivo in ['NO', 'FALSE', '0', 'F']: data_to_save[model_field] = False
                        else: data_to_save[model_field] = None # o default, o errore
                    elif model_field == 'data_conferimento':
                        dt_obj = excel_date_to_datetime(val) # Usa la tua funzione
                        if dt_obj: data_to_save[model_field] = dt_obj.date()
                        else:
                            messages.warning(request, f"Riga {index+2}: Formato data non valido per '{val}'.")
                            valid_row = False
                    elif model_field in ['pezzatura', 'giacenza', 'quantita_conferita']:
                        try:
                            # Rimuovi eventuali simboli di valuta o separatori migliaia se presenti
                            cleaned_val = str(val).replace('€', '').replace('.', '').replace(',', '.').strip()
                            data_to_save[model_field] = float(cleaned_val)
                        except ValueError:
                            messages.warning(request, f"Riga {index+2}: Valore non numerico per '{model_field}': {val}.")
                            valid_row = False
                    else: # Altri campi stringa
                        data_to_save[model_field] = str(val).strip()
                # else: se la colonna mappata non c'è o è vuota, non la includiamo in data_to_save,
                # il modello userà i suoi default (es. blank=True, null=True o default=...)

            if not valid_row or not data_to_save:
                if not data_to_save and valid_row: pass # riga vuota basata su mappatura, ignora
                else: errori_riga.append(f"Riga {index+2}: Dati non validi o mancanti, saltata.")
                continue

            try:
                articolo = Articolo(**data_to_save)
                articolo.full_clean() 
                articolo.save()       
                articoli_creati += 1
            except Exception as e: 
                errori_riga.append(f"Riga {index+2} (dati: {data_to_save}): Errore - {e}")
        
        fs_path = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
        fs = FileSystemStorage(location=fs_path)
        if fs.exists(os.path.basename(uploaded_file_path)):
            fs.delete(os.path.basename(uploaded_file_path))
        
        for key in ['uploaded_file_path', 'file_columns', 'column_mapping']:
            if key in request.session: del request.session[key]

        summary_message_html = f"Importazione terminata. Articoli creati: {articoli_creati}."
        if errori_riga:
            summary_message_html += "<br>Errori riscontrati:<ul>" + "".join(f"<li>{err}</li>" for err in errori_riga) + "</ul>"
            messages.warning(request, summary_message_html, extra_tags='safe') # Usa extra_tags='safe'
        else:
            messages.success(request, summary_message_html)
            
        return redirect('inventory:lista')

    except Exception as e:
        messages.error(request, f"Errore critico durante il processo di importazione: {e}")
        for key in ['uploaded_file_path', 'file_columns', 'column_mapping']:
            if key in request.session: del request.session[key]
        return redirect('inventory:upload_file')

@login_required
@permission_required('inventory.view_articolo', raise_exception=True) # O il permesso più appropriato
def export_articoli(request):
    # ... (come prima) ...
    articolo_resource = ArticoloResource()
    dataset = articolo_resource.export(Articolo.objects.all())
    from django.http import HttpResponse
    response_format = 'xlsx' 
    file_content = dataset.xlsx
    response = HttpResponse(file_content, content_type=f'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="articoli_export.{response_format}"'
    # messages.success(request, "Esportazione completata.") # Il messaggio qui potrebbe non essere visto se il file viene scaricato subito
    return response