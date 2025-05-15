from django.db import models
from django.db.models import Max
from django.utils import timezone # Importa timezone

class Articolo(models.Model):
    numero_sequenziale = models.AutoField(primary_key=True)
    codice_articolo = models.CharField(max_length=100)
    trasposizione = models.CharField(max_length=100, blank=True, null=True) # blank=True se può essere vuoto
    descrizione = models.CharField(max_length=250)
    um = models.CharField(max_length=10)
    pezzatura = models.DecimalField(max_digits=10, decimal_places=2)
    giacenza = models.DecimalField(max_digits=10, decimal_places=2)
    codice_fornitore = models.CharField(max_length=100)
    anagrafica_fornitore = models.CharField(max_length=250)
    scheda_riferimento = models.CharField(max_length=10)
    conta_arrivi = models.IntegerField(editable=False) # Non modificabile direttamente
    # MODIFICATO: Rimuovi auto_now_add per permettere importazione, usa default per creazione manuale
    data_conferimento = models.DateField(default=timezone.now)
    partita_produzione = models.CharField(max_length=250, blank=True, null=True)
    quantita_conferita = models.DecimalField(max_digits=10, decimal_places=2)
    attivo = models.BooleanField(default=True)

    # Rimosso UniqueConstraint perché numero_sequenziale è già primary_key
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['numero_sequenziale'], name='unique_numero_sequenziale')
    #     ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None # Verifica se è un nuovo record

        if is_new: # Solo per nuovi record
            # Calcolo automatico di conta_arrivi
            max_arrivo_obj = Articolo.objects.filter(codice_articolo=self.codice_articolo).aggregate(Max('conta_arrivi'))
            max_arrivo = max_arrivo_obj['conta_arrivi__max']
            self.conta_arrivi = (max_arrivo or 0) + 1

        # Disattiva altri record attivi dello stesso codice_articolo *solo se questo record è attivo e nuovo*
        # o se questo record viene esplicitamente attivato.
        if self.attivo:
            # Crea una query per gli altri articoli attivi
            altri_attivi = Articolo.objects.filter(codice_articolo=self.codice_articolo, attivo=True)
            if not is_new: # Se sto aggiornando, escludo me stesso dalla query
                altri_attivi = altri_attivi.exclude(pk=self.pk)
            altri_attivi.update(attivo=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codice_articolo} - {self.descrizione}"