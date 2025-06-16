from django.contrib import admin
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

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(UtangEntry)
admin.site.register(Payment)
admin.site.register(Category)
admin.site.register(PriceAdjustment)
admin.site.register(Sale)
admin.site.register(SaleItem)
