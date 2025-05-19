# EntrataMerci/app/inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView # DetailView rimosso se non usato
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from .models import Articolo, Deposito, Posizione
from .forms import (
    ArticoloForm, DepositoForm, PosizioneForm, # Assicurati che siano importati
    ArticoloImportForm,
)
from .resources import ArticoloResource

from tablib import Dataset
from django.contrib import messages

# --- Viste ARTICOLO (come definite precedentemente) ---
class ArticoloListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Articolo
    template_name = 'inventory/articolo_list.html' # Cambiato per specificità
    context_object_name = 'articoli'
    permission_required = 'inventory.view_articolo'
    paginate_by = 15 # Esempio di paginazione

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name_plural'] = 'Articoli'
        context['create_url_name'] = 'inventory:articolo_create'
        context['import_url_name'] = 'inventory:articolo_import' # Per il template
        context['export_url_name'] = 'inventory:articolo_export' # Per il template
        context['page_title'] = 'Elenco Articoli'
        return context

class ArticoloCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Articolo
    form_class = ArticoloForm
    template_name = 'inventory/generic_form.html' # Usiamo un form generico
    success_url = reverse_lazy('inventory:articolo_list')
    permission_required = 'inventory.add_articolo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Crea Nuovo Articolo'
        context['page_title'] = 'Nuovo Articolo'
        context['list_url_name'] = 'inventory:articolo_list' # Per il bottone "Annulla"
        return context

class ArticoloUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Articolo
    form_class = ArticoloForm
    template_name = 'inventory/generic_form.html'
    success_url = reverse_lazy('inventory:articolo_list')
    permission_required = 'inventory.change_articolo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Modifica Articolo: {self.object.nome_articolo}'
        context['page_title'] = f'Modifica {self.object.nome_articolo}'
        context['list_url_name'] = 'inventory:articolo_list'
        return context

class ArticoloDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Articolo
    template_name = 'inventory/generic_confirm_delete.html' # Usiamo un confirm_delete generico
    success_url = reverse_lazy('inventory:articolo_list')
    permission_required = 'inventory.delete_articolo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_to_delete'] = self.object
        context['page_title'] = f'Elimina {self.object}'
        context['cancel_url_name'] = 'inventory:articolo_list' # Per il bottone "Annulla"
        return context

# --- Viste DEPOSITO ---
class DepositoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Deposito
    template_name = 'inventory/deposito_list.html' # Template specifico
    context_object_name = 'depositi'
    permission_required = 'inventory.view_deposito'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name_plural'] = 'Depositi'
        context['create_url_name'] = 'inventory:deposito_create'
        context['page_title'] = 'Elenco Depositi'
        # Aggiungi import/export URL se li implementi per Depositi
        return context

class DepositoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Deposito
    form_class = DepositoForm
    template_name = 'inventory/generic_form.html'
    success_url = reverse_lazy('inventory:deposito_list')
    permission_required = 'inventory.add_deposito'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Crea Nuovo Deposito'
        context['page_title'] = 'Nuovo Deposito'
        context['list_url_name'] = 'inventory:deposito_list'
        return context

class DepositoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Deposito
    form_class = DepositoForm
    template_name = 'inventory/generic_form.html'
    success_url = reverse_lazy('inventory:deposito_list')
    permission_required = 'inventory.change_deposito'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Modifica Deposito: {self.object.nome_deposito}'
        context['page_title'] = f'Modifica {self.object.nome_deposito}'
        context['list_url_name'] = 'inventory:deposito_list'
        return context

class DepositoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Deposito
    template_name = 'inventory/generic_confirm_delete.html'
    success_url = reverse_lazy('inventory:deposito_list')
    permission_required = 'inventory.delete_deposito'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_to_delete'] = self.object
        context['page_title'] = f'Elimina {self.object}'
        context['cancel_url_name'] = 'inventory:deposito_list'
        return context

# --- Viste POSIZIONE ---
class PosizioneListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Posizione
    template_name = 'inventory/posizione_list.html' # Template specifico
    context_object_name = 'posizioni'
    permission_required = 'inventory.view_posizione'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name_plural'] = 'Posizioni'
        context['create_url_name'] = 'inventory:posizione_create'
        context['page_title'] = 'Elenco Posizioni'
        # Aggiungi import/export URL se li implementi per Posizioni
        return context

class PosizioneCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Posizione
    form_class = PosizioneForm
    template_name = 'inventory/generic_form.html'
    success_url = reverse_lazy('inventory:posizione_list')
    permission_required = 'inventory.add_posizione'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Crea Nuova Posizione'
        context['page_title'] = 'Nuova Posizione'
        context['list_url_name'] = 'inventory:posizione_list'
        return context

class PosizioneUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Posizione
    form_class = PosizioneForm
    template_name = 'inventory/generic_form.html'
    success_url = reverse_lazy('inventory:posizione_list')
    permission_required = 'inventory.change_posizione'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Modifica Posizione: {self.object}' # __str__ del modello Posizione
        context['page_title'] = f'Modifica {self.object}'
        context['list_url_name'] = 'inventory:posizione_list'
        return context

class PosizioneDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Posizione
    template_name = 'inventory/generic_confirm_delete.html'
    success_url = reverse_lazy('inventory:posizione_list')
    permission_required = 'inventory.delete_posizione'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_to_delete'] = self.object
        context['page_title'] = f'Elimina {self.object}'
        context['cancel_url_name'] = 'inventory:posizione_list'
        return context

# --- Viste IMPORT/EXPORT (Articolo, come definite precedentemente) ---
@login_required
@permission_required('inventory.add_articolo', raise_exception=True)
def import_articoli(request):
    # ... (codice import_articoli come fornito precedentemente, assicurati che usi ArticoloImportForm) ...
    if request.method == 'POST':
        form = ArticoloImportForm(request.POST, request.FILES)
        if form.is_valid():
            # ... (logica di importazione)
            # messages.success(request, 'Dati articoli importati con successo!')
            return redirect('inventory:articolo_list')
    else:
        form = ArticoloImportForm()
    return render(request, 'inventory/generic_import_form.html', {
        'form': form,
        'model_name_plural': 'Articoli',
        'page_title': 'Importa Articoli',
        'list_url_name': 'inventory:articolo_list'
    })

@login_required
@permission_required('inventory.view_articolo', raise_exception=True)
def export_articoli(request):
    # ... (codice export_articoli come fornito precedentemente) ...
    pass

# --- Vista HOME INVENTORY (come definita precedentemente, assicurati sia corretta) ---
@login_required
def home_inventory(request):
    ultimi_articoli = Articolo.objects.order_by('-data_ultima_modifica')[:5]
    numero_articoli = Articolo.objects.count()
    numero_depositi = Deposito.objects.count()
    numero_posizioni = Posizione.objects.count()

    context = {
        'ultimi_articoli': ultimi_articoli,
        'numero_articoli': numero_articoli,
        'numero_depositi': numero_depositi,
        'numero_posizioni': numero_posizioni,
        'url_import_articoli': reverse_lazy('inventory:articolo_import'), # Usato in home_inventory.html
        'url_export_articoli': reverse_lazy('inventory:articolo_export'), # Usato in home_inventory.html
        'page_title': 'Dashboard Inventario'
    }
    return render(request, 'inventory/home_inventory.html', context)