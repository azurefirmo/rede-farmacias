from rest_framework import viewsets, permissions
from .models import Order, SupplierOrder
from .serializers import SaleCreateSerializer, SupplierOrderSerializer
from users.permissions import IsAdmin, IsManager, IsCashier

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return SaleCreateSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Clientes, Caixas, Gerentes e Admin podem vender
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Order.objects.all()
        if user.role in ['MANAGER', 'CASHIER']:
            return Order.objects.filter(branch=user.branch)
        return Order.objects.filter(customer=user) # Cliente só vê suas ordens

class SupplierOrderViewSet(viewsets.ModelViewSet):
    """ Gerentes pedem para Fornecedores """
    serializer_class = SupplierOrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'SUPPLIER':
            return SupplierOrder.objects.filter(supplier=user)
        if user.role in ['ADMIN', 'MANAGER']:
            return SupplierOrder.objects.all()
        return SupplierOrder.objects.none()