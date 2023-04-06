from django.urls import path, include, re_path
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, InvoiceItemViewSet, ItemsInInvoiceViewSet, TransactionViewSet, CompanyViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename="companies")
router.register(r'invoices', InvoiceViewSet, basename="invoices")
router.register(r'invoice_items', InvoiceItemViewSet, basename="invoice_items")
router.register(r'items_in_invoice', ItemsInInvoiceViewSet, basename="items_in_invoice")
router.register(r'transactions', TransactionViewSet, basename="transactions")

# The API URLs are now determined automatically by the router.
urlpatterns = router.urls

urlpatterns += [
    # re_path(r'.*', lambda request: redirect('invoices-home')),
]

