from django.db import models
from django.conf import settings

# Create your models here.

class SupplierOrder(models.Model):
    """ Pedidos feitos da farmácia para o fornecedor """
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, limit_choices_to={'role': 'SUPPLIER'})
    branch = models.ForeignKey('inventory.Branch', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_received = models.BooleanField(default=False)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)

class Order(models.Model):
    class PaymentMethod(models.TextChoices):
        PIX = "PIX", "Pix"
        CREDIT_CARD = "CARD", "Cartão de Crédito"
        DEBIT_CARD = "DEBIT", "Cartão de Débito"
        CASH = "CASH", "Dinheiro"

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    branch = models.ForeignKey('inventory.Branch', on_delete=models.PROTECT)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    nfce_number = models.CharField(max_length=50, blank=True, null=True) # Número da Nota Fiscal
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)