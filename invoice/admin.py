from django.contrib import admin

# Register your models here.
from .models import Invoice, InvoiceItem, InvoiceItems, Transaction, Company

admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(InvoiceItems)
admin.site.register(Transaction)
admin.site.register(Company)
