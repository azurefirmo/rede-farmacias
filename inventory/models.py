from django.db import models

# Create your models here.

class Branch(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    ie = models.CharField(max_length=15, blank=True, null=True, verbose_name="Inscrição Estadual")
    cep = models.CharField(max_length=8)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)  # UF
    is_warehouse = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Branches"


class Product(models.Model):
    name = models.CharField(max_length=255)
    active_principle = models.CharField(max_length=255, blank=True)  # Princípio Ativo
    barcode = models.CharField(max_length=13, unique=True)  # EAN-13
    ms_registration = models.CharField(max_length=13, verbose_name="Registro MS (ANVISA)")
    ncm = models.CharField(max_length=8, verbose_name="NCM")  # Para Nota Fiscal

    price_retail = models.DecimalField(max_digits=10, decimal_places=2)
    price_wholesale = models.DecimalField(max_digits=10, decimal_places=2)

    requires_prescription = models.BooleanField(default=False)
    is_controlled = models.BooleanField(default=False)  # Medicamento Controlado (Portaria 344)

    def __str__(self):
        return self.name


class Stock(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    batch_number = models.CharField(max_length=50)  # Lote
    expiry_date = models.DateField()  # Validade do Lote

    class Meta:
        unique_together = ('branch', 'product', 'batch_number')