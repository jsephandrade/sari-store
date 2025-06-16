from rest_framework import serializers
from .models import Product, Customer, UtangEntry, Payment


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('date_paid',)


class UtangEntrySerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = UtangEntry
        fields = '__all__'

    def create(self, validated_data):
        utang = super().create(validated_data)
        utang.total_amount = utang.product.price * utang.quantity
        utang.save()
        return utang
