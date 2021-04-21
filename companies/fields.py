from django.forms import fields
from django.forms import widgets
from typing import *


class Select(widgets.Select):
    template_name = 'companies/widgets/select.html'

    # def __init__(self, search_url, all_url, fields, repr_format, attrs=None) -> None:
    def __init__(self, search_url, all_url, repr_format, attrs=None) -> None:
        self.repr_format = repr_format
        self.search_url = search_url
        self.all_url = all_url
        super().__init__(attrs=attrs)
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # set urls
        context['repr_format'] = self.repr_format
        context['search_url'] = self.search_url
        context['all_url'] = self.all_url

        if self.allow_multiple_selected:
            context['widget']['attrs']['multiple'] = True
        return context
    

class SearchableSelectField(fields.ChoiceField):
    widget = Select
    # def __init__(self, search_url, all_url, fields, repr_format,*args, **kwargs) -> None:
    def __init__(self, search_url, all_url, repr_format, *args, **kwargs) -> None:
        self.widget = Select(search_url, all_url, repr_format)
        super().__init__(*args, **kwargs)

    