# EntrataMerci/app/inventory/models.py
from django.db import models
from django.utils import timezone

class Deposito(models.Model):
    nome_deposito = models.CharField(max_length=100, unique=True)
    indirizzo = models.CharField(max_length=255, blank=True, null=True)
    # Aggiungi altri campi rilevanti per il deposito, es. responsabile, note, ecc.

    def __str__(self):
        return self.nome_deposito

    class Meta:
        verbose_name = "Deposito"
        verbose_name_plural = "Depositi"
        ordering = ['nome_deposito']

class Posizione(models.Model):
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE, related_name='posizioni_deposito') # Nome related_name cambiato
    nome_posizione = models.CharField(max_length=100, help_text="Es. Scaffale A, Ripiano 3, Settore Nord")
    # Aggiungi altri campi rilevanti per la posizione, es. codice a barre, tipo di scaffale, ecc.

    def __str__(self):
        return f"{self.nome_posizione} (Deposito: {self.deposito.nome_deposito})"

    class Meta:
        verbose_name = "Posizione"
        verbose_name_plural = "Posizioni"
        unique_together = ('deposito', 'nome_posizione') # Una posizione ha un nome univoco all'interno di un deposito
        ordering = ['deposito__nome_deposito', 'nome_posizione']


class Articolo(models.Model):
    TIPOLOGIA_ARTICOLO_CHOICES = [
        ('MAT_PRIMA', 'Materia Prima'),
        ('SEMILAVORATO', 'Semilavorato'),
        ('PROD_FINITO', 'Prodotto Finito'),
        ('CONSUMABILE', 'Materiale di Consumo'),
        ('RICAMBIO', 'Ricambio'),
        ('ATTREZZATURA', 'Attrezzatura'),
        ('ALTRO', 'Altro'),
    ]
    UNITA_DI_MISURA_CHOICES = [
        ('PZ', 'Pezzi'),
        ('KG', 'Chilogrammi'),
        ('LT', 'Litri'),
        ('MT', 'Metri'),
        ('MQ', 'Metri Quadri'),
        ('MC', 'Metri Cubi'),
        ('PALLET', 'Pallet'),
        ('SCATOLA', 'Scatola'),
        ('ALTRO', 'Altro'),
    ]

    numero_sequenziale = models.CharField(max_length=50, unique=True, help_text="Codice univoco dell'articolo (es. SKU, Part Number)")
    nome_articolo = models.CharField(max_length=200)
    descrizione = models.TextField(blank=True, null=True)
    tipologia_articolo = models.CharField(max_length=20, choices=TIPOLOGIA_ARTICOLO_CHOICES, default='ALTRO')
    unita_di_misura = models.CharField(max_length=10, choices=UNITA_DI_MISURA_CHOICES, default='PZ')
    
    prezzo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantita = models.IntegerField(default=0, help_text="Quantità totale disponibile in magazzino per questa specifica posizione/deposito") # Modificato help_text
    
    # CAMPI CHIAVE MODIFICATI:
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT, null=True, blank=True, related_name='articoli')
    posizione = models.ForeignKey(Posizione, on_delete=models.PROTECT, null=True, blank=True, related_name='articoli')
    # NOTA: Considera se un articolo PUO' esistere senza deposito/posizione o se sono obbligatori.
    # Se obbligatori, rimuovi null=True, blank=True.
    # on_delete=models.PROTECT impedisce l'eliminazione di un deposito/posizione se ci sono articoli associati.
    # Valuta se CASCADE o SET_NULL è più appropriato per il tuo caso d'uso.

    data_inserimento = models.DateTimeField(default=timezone.now)
    data_ultima_modifica = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome_articolo} ({self.numero_sequenziale})"

    class Meta:
        verbose_name = "Articolo"
        verbose_name_plural = "Articoli"
        ordering = ['nome_articolo']