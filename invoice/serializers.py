from rest_framework import serializers
from .models import Invoice, InvoiceItem, ItemsInInvoice, Transaction, Company



class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__" 


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = "__all__"

class ItemsInInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsInInvoice
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
