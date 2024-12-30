from itertools import chain
from django.db import models
from typing import Dict, Any


class ChainedQuerysetsWithCount:
    def __init__(self, *querysets):
        self.chained_queryset = chain(*querysets)
        self.total_count = sum(map(lambda queryset: queryset.count(), querysets))

    def __iter__(self):
        return self.chained_queryset
    
    def count(self):
        return self.total_count


def model_field_to_form_meta(field: models.Field, load_fk_options=False) -> Dict[str, Any]:
    """
    Maps a Django model field to its HTML and Python metadata using a match statement.
    Includes options for fields with choices or foreign keys.
    
    Args:
        field (Field): A Django model field instance.
        
    Returns:
        dict: A dictionary containing the field name, Django field type, HTML tag, 
              HTML input type, Python type, and options.
    """
    match field:
        case models.TextField():
            html_tag = "textarea"
            html_tag_type = None
            python_type = "str"
        case models.CharField():
            html_tag = "input"
            html_tag_type = "text"
            python_type = "str"
        case models.EmailField():
            html_tag = "input"
            html_tag_type = "email"
            python_type = "str"
        case models.URLField():
            html_tag = "input"
            html_tag_type = "url"
            python_type = "str"
        case models.BooleanField():
            html_tag = "input"
            html_tag_type = "checkbox"
            python_type = "bool"
        case models.DateField():
            html_tag = "input"
            html_tag_type = "date"
            python_type = "datetime.date"
        case models.DateTimeField():
            html_tag = "input"
            html_tag_type = "datetime-local"
            python_type = "datetime.datetime"
        case models.TimeField():
            html_tag = "input"
            html_tag_type = "time"
            python_type = "datetime.time"
        case models.DecimalField():
            html_tag = "input"
            html_tag_type = "number"
            python_type = "decimal.Decimal"
        case models.IntegerField():
            html_tag = "input"
            html_tag_type = "number"
            python_type = "int"
        case models.SlugField():
            html_tag = "input"
            html_tag_type = "text"
            python_type = "str"
        case models.ForeignKey():
            html_tag = "select"
            html_tag_type = None
            python_type = "int"  # Typically refers to the related model's primary key
        case _:
            html_tag = "input"
            html_tag_type = "text"
            python_type = "str"


    # Check if the field has choices
    if field.choices:
        html_tag = "select"
        html_tag_type = None  # Select tag doesn't use a "type" attribute
        options = [{"value": choice[0], "display": choice[1]} for choice in field.choices]
    else:
        options = None
    
    if load_fk_options and isinstance(field, models.ForeignKey):
        related_model = field.related_model
        options = [
            {"value": obj.pk, "display": str(obj)} for obj in related_model.objects.all()
        ]

    # Return metadata
    return {
        # "python_type": python_type,
        # "django_field_type": field.__class__.__name__,
        "name": field.name,
        "label": field.verbose_name,
        "html_tag": html_tag,
        "html_tag_type": html_tag_type,
        "options": options,
    }
