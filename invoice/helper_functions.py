from .models import Invoice, InvoiceItem, ItemsInInvoice

ROUND_TO = 2


############################################################################################################
# For Items in invoice
def get_amount_for_item_in_invoice(item_in_invoice):
    res = item_in_invoice.quantity * item_in_invoice.rate
    return round(res, ROUND_TO)

def get_vat_for_item_in_invoice(item_in_invoice):
    if item_in_invoice.vat_percent is None:
        res = 0
    else:
        res = get_amount_for_item_in_invoice(item_in_invoice) * (item_in_invoice.vat_percent / 100)
    return round(res, ROUND_TO)


def get_subtotal_for_items_in_invoice(items_in_invoice):
    res = 0
    for item in items_in_invoice:
        res += get_amount_for_item_in_invoice(item)
    return round(res, ROUND_TO)

def get_total_vat_for_items_in_invoice(items_in_invoice):
    res = 0
    for item in items_in_invoice:
        res += get_vat_for_item_in_invoice(item)
    return round(res, ROUND_TO)

def get_total_for_items_in_invoice(items_in_invoice):
    res = 0
    for item in items_in_invoice:
        res += get_amount_for_item_in_invoice(item) + get_vat_for_item_in_invoice(item)
    return round(res, ROUND_TO)


############################################################################################################
# For Invoice
def get_amount_for_invoice(invoice):
    items_in_invoice = ItemsInInvoice.objects.filter(invoice_id=invoice)
    return get_total_for_items_in_invoice(items_in_invoice) - invoice.discount

