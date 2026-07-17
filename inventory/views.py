from rest_framework import viewsets, permissions
from .models import Branch, Product, Stock
from .serializers import BranchSerializer, ProductSerializer, StockSerializer
from users.permissions import IsAdmin, IsManager, IsStocker

# Create your views here.

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdmin]  # Apenas admin cria/edita filiais


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]  # Apenas admin mexe no catálogo global de produtos
        return [permissions.IsAuthenticated()]


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [(IsAdmin | IsManager | IsStocker)()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Stock.objects.all()
        if user.branch:
            return Stock.objects.filter(branch=user.branch)
        return Stock.objects.none()