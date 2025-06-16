from rest_framework import viewsets, status, generics, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.contrib.auth.models import User

from .models import Product, Customer, UtangEntry, Payment
from .serializers import (
    ProductSerializer,
    CustomerSerializer,
    UtangEntrySerializer,
    PaymentSerializer,
    RegisterSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class UtangEntryViewSet(viewsets.ModelViewSet):
    queryset = UtangEntry.objects.select_related(
        "customer", "product"
    ).prefetch_related("payments")
    serializer_class = UtangEntrySerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        qs = self.queryset
        customer_id = self.request.query_params.get("customer")
        status = self.request.query_params.get("status")
        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        if status:
            qs = qs.filter(status=status)
        return qs


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("utang_entry")
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        payment = serializer.instance
        utang = payment.utang_entry
        total_paid = utang.payments.aggregate(total=Sum("amount_paid"))["total"] or 0
        if total_paid >= utang.total_amount:
            utang.status = "paid"
            utang.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class SummaryViewSet(viewsets.ViewSet):
    def list(self, request):
        total_products = Product.objects.count()
        total_utang = (
            UtangEntry.objects.filter(status="pending").aggregate(
                total=Sum("total_amount")
            )["total"]
            or 0
        )
        recent_payments = Payment.objects.order_by("-date_paid")[:5].values(
            "utang_entry__customer__name", "amount_paid", "date_paid"
        )
        return Response(
            {
                "total_products": total_products,
                "total_utang": total_utang,
                "recent_payments": list(recent_payments),
            }
        )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
