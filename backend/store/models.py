from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name="products", blank=True)

    def adjust_price(self, new_price):
        PriceAdjustment.objects.create(product=self, old_price=self.price, new_price=new_price)
        self.price = new_price
        self.save(update_fields=["price"])

    def __str__(self):
        return self.name


class PriceAdjustment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_adjustments")
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_changed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name}: {self.old_price} -> {self.new_price}"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    segment = models.CharField(max_length=50, blank=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def outstanding_balance(self):
        total = (
            self.utangentry_set.filter(status="pending").aggregate(sum=models.Sum("total_amount"))
            ["sum"]
            or 0
        )
        paid = (
            Payment.objects.filter(utang_entry__customer=self).aggregate(sum=models.Sum("amount_paid"))
            ["sum"]
            or 0
        )
        return total - paid


class UtangEntry(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.customer.name} - {self.product.name}"


class Payment(models.Model):
    utang_entry = models.ForeignKey(
        UtangEntry, on_delete=models.CASCADE, related_name="payments"
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.utang_entry} - {self.amount_paid}"


class Sale(models.Model):
    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("card", "Card"),
        ("mobile", "Mobile"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale #{self.id}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
