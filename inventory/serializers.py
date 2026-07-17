from rest_framework import serializers
from .models import Branch, Product, Stock

# Create your models here.

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Stock
        fields = ['id', 'branch', 'product', 'product_name', 'quantity', 'batch_number', 'expiry_date']