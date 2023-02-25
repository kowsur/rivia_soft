from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, InvoiceItemViewSet, InvoiceItemsViewSet, TransactionViewSet, CompanyViewSet, invoice_index

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename="companies")
router.register(r'invoices', InvoiceViewSet, basename="invoices")
router.register(r'invoice_items', InvoiceItemViewSet, basename="invoice_items")
router.register(r'items_in_invoice', InvoiceItemsViewSet, basename="items_in_invoice")
router.register(r'transactions', TransactionViewSet, basename="transactions")

# The API URLs are now determined automatically by the router.
urlpatterns = router.urls

urlpatterns += [
    path('index/', invoice_index, name="invoice-index")
]