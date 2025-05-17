# EntrataMerci/app/inventory/models.py
from django.db import models
from django.utils import timezone

class Deposito(models.Model):
    nome_deposito = models.CharField(max_length=100, unique=True)
    indirizzo = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.nome_deposito
    class Meta:
        verbose_name = "Deposito"
        verbose_name_plural = "Depositi"
        ordering = ['nome_deposito']

class Posizione(models.Model):
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE, related_name='posizioni_deposito')
    nome_posizione = models.CharField(max_length=100, help_text="Es. Scaffale A, Ripiano 3, Settore Nord")
    def __str__(self):
        return f"{self.nome_posizione} (Deposito: {self.deposito.nome_deposito})"
    class Meta:
        verbose_name = "Posizione"
        verbose_name_plural = "Posizioni"
        unique_together = ('deposito', 'nome_posizione')
        ordering = ['deposito__nome_deposito', 'nome_posizione']

class Articolo(models.Model):
    TIPOLOGIA_ARTICOLO_CHOICES = [
        ('MAT_PRIMA', 'Materia Prima'), ('SEMILAVORATO', 'Semilavorato'),
        ('PROD_FINITO', 'Prodotto Finito'), ('CONSUMABILE', 'Materiale di Consumo'),
        ('RICAMBIO', 'Ricambio'), ('ATTREZZATURA', 'Attrezzatura'), ('ALTRO', 'Altro'),
    ]
    UNITA_DI_MISURA_CHOICES = [
        ('PZ', 'Pezzi'), ('KG', 'Chilogrammi'), ('LT', 'Litri'), ('MT', 'Metri'),
        ('MQ', 'Metri Quadri'), ('MC', 'Metri Cubi'), ('PALLET', 'Pallet'),
        ('SCATOLA', 'Scatola'), ('ALTRO', 'Altro'),
    ]

    numero_sequenziale = models.CharField(max_length=50, unique=True, help_text="Codice univoco dell'articolo (es. SKU, Part Number)")
    # Se 'codice_articolo' è diverso e serve, aggiungilo:
    # codice_articolo_custom = models.CharField(max_length=50, blank=True, null=True, help_text="Altro codice articolo")
    nome_articolo = models.CharField(max_length=200)
    descrizione = models.TextField(blank=True, null=True)
    tipologia_articolo = models.CharField(max_length=20, choices=TIPOLOGIA_ARTICOLO_CHOICES, default='ALTRO')
    unita_di_misura = models.CharField(max_length=10, choices=UNITA_DI_MISURA_CHOICES, default='PZ')
    
    prezzo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantita = models.IntegerField(default=0, help_text="Quantità totale disponibile")
    
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT, null=True, blank=True, related_name='articoli')
    posizione = models.ForeignKey(Posizione, on_delete=models.PROTECT, null=True, blank=True, related_name='articoli')

    data_inserimento = models.DateTimeField(default=timezone.now, verbose_name="Data Conferimento/Inserimento") # verbose_name per l'admin
    data_ultima_modifica = models.DateTimeField(auto_now=True)
    
    attivo = models.BooleanField(default=True) # Aggiunto campo 'attivo'

    # Campi per search_fields, se necessari:
    codice_fornitore = models.CharField(max_length=50, blank=True, null=True)
    partita_produzione = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nome_articolo} ({self.numero_sequenziale})"

    # Se 'conta_arrivi' è un campo calcolato sul modello (es. da un related_name di un altro modello 'Arrivo')
    # Esempio: se avessi un modello Arrivo con ForeignKey ad Articolo:
    # @property
    # def numero_di_arrivi(self):
    #     return self.arrivi_set.count() # Assumendo related_name='arrivi_set' o default

    class Meta:
        verbose_name = "Articolo"
        verbose_name_plural = "Articoli"
        ordering = ['nome_articolo']