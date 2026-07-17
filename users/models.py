from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        SUPPLIER = "SUPPLIER", "Fornecedor"
        MANAGER = "MANAGER", "Gerente"
        PHARMACIST = "PHARMACIST", "Farmacêutico"
        STOCKER = "STOCKER", "Repositor"
        CASHIER = "CASHIER", "Operador de Caixa"
        RETAIL_CUSTOMER = "RETAIL", "Cliente Varejo"
        WHOLESALE_CUSTOMER = "WHOLESALE", "Cliente Atacado"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RETAIL_CUSTOMER)
    cpf_cnpj = models.CharField(max_length=14, unique=True, verbose_name="CPF ou CNPJ")
    phone = models.CharField(max_length=15)

    # Específico para Farmacêuticos
    crf_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Registro CRF")
    crf_state = models.CharField(max_length=2, blank=True, null=True, verbose_name="UF do CRF")

    branch = models.ForeignKey('inventory.Branch', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"