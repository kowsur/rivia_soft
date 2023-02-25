from django.shortcuts import render
from rest_framework import viewsets, permissions, renderers, mixins, decorators, response
from .models import Invoice, InvoiceItem, InvoiceItems, Transaction, Company
from .serializers import InvoiceSerializer, InvoiceItemSerializer, TransactionSerializer, CompanySerializer


from companies.url_variables import APPLICATION_NAME, URL_NAMES, URL_PATHS, Full_URL_PATHS_WITHOUT_ARGUMENTS, URL_NAMES_PREFIXED_WITH_APP_NAME
from companies.url_variables import *

application_name = APPLICATION_NAME
# these path names will be passed to templates to use in the navbar links
URLS = {
  'home': f'{application_name}:home',

  **Full_URL_PATHS_WITHOUT_ARGUMENTS.get_dict(),
  **URL_NAMES_PREFIXED_WITH_APP_NAME.get_dict()
}



def invoice_index(request):
    context = {
        **URLS
    }
    return render(request, 'invoice/index.html', context)


class InvoiceViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    renderer_classes = [renderers.JSONRenderer]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=False, methods=['get'])
    def search(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        query = request.query_params.get('q', None)
        if query is not None:
            queryset = queryset.filter(customer_email__icontains=query)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class InvoiceItemViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    renderer_classes = [renderers.JSONRenderer]
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class InvoiceItemsViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    renderer_classes = [renderers.JSONRenderer]
    queryset = InvoiceItems.objects.all()
    serializer_class = InvoiceItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    renderer_classes = [renderers.JSONRenderer]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    renderer_classes = [renderers.JSONRenderer]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

