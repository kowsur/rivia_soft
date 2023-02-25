from django.db import models
from companies.models import Selfassesment, Limited
from django.core.validators import MinValueValidator, MaxValueValidator



class Company(models.Model):
    class Meta:
        verbose_name_plural = "Companies"
        constraints = [
                models.CheckConstraint(check=models.Q(selfassesment__isnull=True) | models.Q(limited__isnull=True), name='limited_or_selfassesment_per_row'),
            ]

    selfassesment = models.ForeignKey(Selfassesment, on_delete=models.CASCADE, null=True, blank=True)
    limited = models.ForeignKey(Limited, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.company)


    @property
    def company(self):
        return self.selfassesment if self.selfassesment else self.limited
    


class Invoice(models.Model):
    invoice_from = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invoice_from')
    invoice_to = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invoice_to')
    customer_email = models.CharField(max_length=100)
    billing_address = models.CharField(max_length=255)
    remarks = models.TextField()

    creation_timestamp = models.DateTimeField(auto_now_add=True)
    service_date = models.DateTimeField()
    due_date = models.DateTimeField()

    amount = models.FloatField(default=0)
    discount = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"From: {self.invoice_from}, To: {self.invoice_to}, SD: {self.service_date}, DD: {self.due_date}"


class InvoiceItem(models.Model):
    name = models.CharField(max_length=255, default='')
    description = models.TextField()
    rate = models.FloatField()
    vat_percent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default=None)

    def __str__(self) -> str:
        return f"Name: {self.name}, Rate: {self.rate}, Vat Percent: {self.vat_percent}"


class InvoiceItems(models.Model):
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invoice_item_id = models.ForeignKey(InvoiceItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"Id: {self.invoice_id}, Item Id: {self.invoice_item_id}"


class Transaction(models.Model):
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    customer_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_types = (
        ("CREDIT", "CREDIT"),
        ("DEBIT", "DEBIT"),
    )
    transaction_type = models.CharField(max_length=100, choices=transaction_types, default="CREDIT")
    current_balance = models.FloatField(default=0)
    amount = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"Type: {self.transaction_type}, Amount: {self.current_balance}, Current Balance: {self.amount}"
