from rest_framework import serializers
from .models import Order, OrderItem, SupplierOrder
from inventory.models import Stock
from django.db import transaction
from datetime import date

# Create your models here.

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'quantity', 'unit_price']
        read_only_fields = ['unit_price']


class SaleCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'branch', 'payment_method', 'items', 'total', 'created_at']
        read_only_fields = ['total', 'created_at']

    def validate(self, data):
        """ Valida se há estoque disponível em qualquer lote daquela filial """
        branch = data['branch']
        for item in data['items']:
            total_stock = Stock.objects.filter(
                branch=branch,
                product=item['product'],
                expiry_date__gt=date.today()  # Apenas produtos não vencidos
            ).aggregate(total=models.Sum('quantity'))['total'] or 0

            if total_stock < item['quantity']:
                raise serializers.ValidationError(
                    f"Estoque insuficiente para {item['product'].name}. Disponível: {total_stock}"
                )
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        branch = validated_data['branch']
        user = self.context['request'].user

        with transaction.atomic():
            order = Order.objects.create(
                customer=user,
                branch=branch,
                payment_method=validated_data['payment_method'],
                total=0
            )

            total_order = 0
            for item_data in items_data:
                product = item_data['product']
                qty_to_reduce = item_data['quantity']

                # Regra de negócio: Baixar do lote que vence MAIS CEDO (FEFO)
                available_batches = Stock.objects.filter(
                    branch=branch,
                    product=product,
                    expiry_date__gt=date.today(),
                    quantity__gt=0
                ).order_by('expiry_date')

                for stock in available_batches:
                    if qty_to_reduce <= 0: break

                    if stock.quantity >= qty_to_reduce:
                        stock.quantity -= qty_to_reduce
                        stock.save()
                        qty_to_reduce = 0
                    else:
                        qty_to_reduce -= stock.quantity
                        stock.quantity = 0
                        stock.save()

                # Definição de preço (Varejo vs Atacado)
                price = product.price_wholesale if user.role == "WHOLESALE" else product.price_retail

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data['quantity'],
                    unit_price=price
                )
                total_order += (price * item_data['quantity'])

            order.total = total_order
            order.save()
            return order


class SupplierOrderSerializer(serializers.ModelSerializer):
    """ Serializer para pedidos de reposição ao fornecedor """

    class Meta:
        model = SupplierOrder
        fields = '__all__'