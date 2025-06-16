from rest_framework import viewsets, status, generics, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User

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
from .serializers import (
    ProductSerializer,
    CustomerSerializer,
    UtangEntrySerializer,
    PaymentSerializer,
    RegisterSerializer,
    CategorySerializer,
    PriceAdjustmentSerializer,
    SaleSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PriceAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = PriceAdjustment.objects.select_related("product")
    serializer_class = PriceAdjustmentSerializer


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


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.prefetch_related("items")
    serializer_class = SaleSerializer


class SummaryViewSet(viewsets.ViewSet):
    def list(self, request):
        total_sales = Sale.objects.aggregate(total=Sum("total_amount"))["total"] or 0
        outstanding_balances = (
            UtangEntry.objects.filter(status="pending").aggregate(total=Sum("total_amount"))["total"]
            or 0
        )
        new_customers = Customer.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=30)).count()
        return Response(
            {
                "total_sales": total_sales,
                "outstanding_balances": outstanding_balances,
                "new_customers": new_customers,
            }
        )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
