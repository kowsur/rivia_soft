from django import forms
from django.forms import widgets
from .models import Selfassesment
from typing import *


class Select(widgets.ChoiceWidget):
    template_name = 'companies/widgets/select.html'
    option_template_name = 'companies/widgets/select_option.html'

    # def __init__(self, search_url, all_url, fields, repr_format, attrs=None) -> None:
    def __init__(self, search_url, all_url, repr_format, *args, attrs=None, model=None, choices=None, fk_field=None,**kwargs) -> None:
        self.repr_format = repr_format
        self.search_url = search_url
        self.all_url = all_url
        self.model = model
        self.fk_field = fk_field
        if self.fk_field==None:
            self.fk_field = self.model._meta.pk.name
        if kwargs.get('label'):
            del kwargs['label']

        super().__init__(choices=choices)
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if self.allow_multiple_selected:
            context['widget']['attrs']['multiple'] = True
        
        # set urls
        context['repr_format'] = self.repr_format
        context['search_url'] = self.search_url
        context['all_url'] = self.all_url
        # get pk field
        # print(self.model._meta.pk.name)

        query = {self.fk_field: value}
        context['value'] = ''
        if not query=={self.fk_field: None}:
            print(self.model, query, name,  value)
            context['value'] = self.model.objects.get(**query)
        return context

class SearchableModelField(forms.ModelChoiceField):
    widget = Select
    # def __init__(self, search_url, all_url, fields, repr_format,*args, **kwargs) -> None:
    def __init__(self, search_url, all_url, repr_format, *args, model=None, choices=None, fk_field=None, **kwargs) -> None:
        self.widget = Select(search_url, all_url, repr_format, *args, model=model, choices=choices, fk_field=fk_field,**kwargs)
        super().__init__(*args, **kwargs)
