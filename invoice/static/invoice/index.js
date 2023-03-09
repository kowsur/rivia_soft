import { openModal, closeModal } from '/static/invoice/Modal.js';
import { textToHTML, OPTIONS, GET, POST, PUT, PATCH, DELETE } from '/static/invoice/utils.js';

closeModal();


// invoice
const invoiceContainer = document.querySelector('#invoice');
const invoiceRowTemplate = invoiceContainer.querySelector('template');

const invoiceItemContainer = document.querySelector('#invoice-item');
const invoiceItemRowTemplate = invoiceItemContainer.querySelector('template');

const transactionContainer = document.querySelector('#transaction');
const transactionRowTemplate = transactionContainer.querySelector('template');



const ENDPOINTS = await getEndPoints()

let invoices = await getInvoices()

getInvoiceItems()
getItemsInInvoice()
getTransactions()


async function getEndPoints() {
    const response = await fetch('/invoice');
    const data = await response.json();
    return data;
}

async function getInvoices(){
    const invoices = await GET(ENDPOINTS.invoices);
    return invoices;
}
async function getInvoiceItems(){
    const invoices = await GET(ENDPOINTS.invoice_items);
    return invoices;
}
async function getTransactions(){
    const invoices = await GET(ENDPOINTS.transactions);
    return invoices;
}
async function getItemsInInvoice(){
    const invoices = await GET(ENDPOINTS.items_in_invoice);
    return invoices;
}
