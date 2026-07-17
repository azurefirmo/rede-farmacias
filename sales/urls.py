from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, SupplierOrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'supplier-orders', SupplierOrderViewSet, basename='supplier-orders')

urlpatterns = [
    path('', include(router.urls)),
]