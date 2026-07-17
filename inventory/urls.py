from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BranchViewSet, ProductViewSet, StockViewSet

router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branches')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'stock', StockViewSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
]