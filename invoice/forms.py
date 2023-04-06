from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from itertools import chain
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from companies.fields import SearchableModelField, Select, Fieldset

from .models import Invoice, Transaction, InvoiceItem, Company

# Uncomment the following line before database migrations
# from .dummy_class import *


def get_date_today(date_format = '%Y-%m-%d'):
    today = timezone.datetime.strftime(timezone.now(), date_format)
    return today



class InvoiceCreationForm(forms.ModelForm):
    invoice_to = SearchableModelField(
        queryset=Company.objects.all(),
        label = 'Invoice to',
        search_url = '/invoice/companies/formatted_search/',
        all_url = '/invoice/companies/formatted_all/',
        repr_format = r'{fields.formatted}',
        model=Company,
        choices=Company.objects.all(),
        fk_field='id',
        empty_label=None,
        disabled=False,
        required=True,
        render_options=True
        )
    
    service_date = forms.DateField(
        label='Service date',
        widget=forms.DateInput(attrs={'type': 'date', 'value': get_date_today, 'placehoder': 'Service date'})
    )
    due_date = forms.DateField(
        label='Due date',
        widget=forms.DateInput(attrs={'type': 'date', 'value': get_date_today, 'placehoder': 'Due date'})
    )
    
    class Meta:
        model = Invoice
        fields = (
            "invoice_to",
            # "customer_email",
            # "billing_address",
            "remarks",

            # "creation_timestamp",
            "service_date",
            "due_date",

            # "amount",
            "discount",
            "is_paid"
            )

class InvoiceChangeForm(forms.ModelForm):
    invoice_to = SearchableModelField(
        queryset=Company.objects.all(),
        label = 'Invoice to',
        search_url = '/invoice/companies/formatted_search/',
        all_url = '/invoice/companies/formatted_all/',
        repr_format = r'{fields.formatted}',
        model=Company,
        choices=Company.objects.all(),
        fk_field='id',
        empty_label=None,
        disabled=True,
        required=False,
        render_options=False
        )
    
    service_date = forms.DateField(
        label='Service date',
        widget=forms.DateInput(attrs={'type': 'date', 'value': get_date_today, 'placehoder': 'Service date'})
    )
    due_date = forms.DateField(
        label='Due date',
        widget=forms.DateInput(attrs={'type': 'date', 'value': get_date_today, 'placehoder': 'Due date'})
    )
    class Meta:
        model = Invoice
        fields = (
            "invoice_to",
            # "customer_email",
            # "billing_address",
            "remarks",

            # "creation_timestamp",
            "service_date",
            "due_date",

            # "amount",
            "discount",
            "is_paid"
            )

class InvoiceDeleteForm(forms.ModelForm):
    agree = forms.BooleanField(label='I want to proceed.', required=True)
    class Meta:
        model = Invoice
        fields = ()



class InvoiceItemCreationForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = (
            "name",
            "description",
            "rate",
            "vat_percent",
            )

class InvoiceItemChangeForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = (
            "name",
            "description",
            "rate",
            "vat_percent",
            )

class InvoiceItemDeleteForm(forms.ModelForm):
    agree = forms.BooleanField(label='I want to proceed.', required=True)
    class Meta:
        model = InvoiceItem
        fields = ()



class TransactionCreationForm(forms.ModelForm):
    invoice_reference_id = SearchableModelField(
        queryset=Invoice.objects.all(),
        label = 'Invoice Reference',
        search_url = '/invoice/invoices/formatted_search/',
        all_url = '/invoice/invoices/formatted_all/',
        repr_format = r'{fields.formatted}',
        model=Invoice,
        choices=Invoice.objects.all(),
        fk_field='id',
        empty_label=None,
        disabled=False,
        required=True,
        render_options=True
        )
    transaction_from = SearchableModelField(
        queryset=Company.objects.all(),
        label = 'Transaction from',
        search_url = '/invoice/companies/formatted_search/',
        all_url = '/invoice/companies/formatted_all/',
        repr_format = r'{fields.formatted}',
        model=Company,
        choices=Company.objects.all(),
        fk_field='id',
        empty_label=None,
        disabled=False,
        required=True,
        render_options=True
        )
    class Meta:
        model = Transaction
        fields = (
            "invoice_reference_id",
            "transaction_from",
            "transaction_type",
            "amount",
            # "timestamp",
            # "current_balance",
            )

class TransactionChangeForm(forms.ModelForm):
    invoice_reference_id = SearchableModelField(
        queryset=Invoice.objects.all(),
        label = 'Invoice Reference',
        search_url = '/invoice/invoices/formatted_search/',
        all_url = '/invoice/invoices/formatted_all/',
        repr_format = r'{fields.formatted}',
        model=Invoice,
        choices=Invoice.objects.all(),
        fk_field='id',
        empty_label=None,
        disabled=True,
        required=False,
        render_options=False
        )
    transaction_from = SearchableModelField(
        queryset=Company.objects.all(),
        label = 'Transaction from',
        search_url = '/invoice/companies/formatted_search/',
        all_url = '/invoice/companies/formatted_all/',
        repr_format = r'{fields.formatted}',
        model=Company,
        choices=Company.objects.all(),
        fk_field='id',
        empty_label=None,
        disabled=True,
        required=False,
        render_options=False
        )
    class Meta:
        model = Transaction
        fields = (
            "invoice_reference_id",
            "transaction_from",
            "transaction_type",
            "amount",
            # "timestamp",
            # "current_balance",
            )

class TransactionDeleteForm(forms.ModelForm):
    agree = forms.BooleanField(label='I want to proceed.', required=True)
    class Meta:
        model = Transaction
        fields = ()
