from django.contrib import admin
from .models import Product, Customer, UtangEntry, Payment

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(UtangEntry)
admin.site.register(Payment)
