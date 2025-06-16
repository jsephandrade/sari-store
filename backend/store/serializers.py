from rest_framework import serializers
from django.db import models
from .models import (
    Product,
    Customer,
    UtangEntry,
    Payment,
    Category,
    PriceAdjustment,
    Sale,
    SaleItem,
)
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PriceAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAdjustment
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("date_paid",)


class UtangEntrySerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = UtangEntry
        fields = "__all__"

    def create(self, validated_data):
        utang = super().create(validated_data)
        utang.total_amount = utang.product.price * utang.quantity
        utang.save()
        return utang


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["product", "quantity", "price"]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ["id", "customer", "payment_method", "total_amount", "date", "items"]
        read_only_fields = ["total_amount", "date"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        sale = Sale.objects.create(**validated_data)
        total = 0
        for item in items_data:
            product = item["product"]
            SaleItem.objects.create(sale=sale, product=product, quantity=item["quantity"], price=product.price)
            product.stock = models.F("stock") - item["quantity"]
            product.save(update_fields=["stock"])
            total += product.price * item["quantity"]
        sale.total_amount = total
        sale.save(update_fields=["total_amount"])
        return sale


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
