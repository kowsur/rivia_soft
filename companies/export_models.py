from django.db.models.fields.related import ForeignKey
from django.db.models import Model
from .html_generator import get_header_name_from_field_name, get_field_names_from_model, is_includeable
import csv
from pprint import pp

def get_nested_attr(obj, attr, default=None, attr_split_on='.'):
    """Filter tag to get python object's attributes.
    Supportes nested attributes separated by '.'.
    If attribute doesn't exists returns None as default.
    """
    attrs = attr.split(attr_split_on)
    value = obj
    for attr in attrs:
        if hasattr(value, 'get'):
            value = value.get(attr, default)
        else:
            value = getattr(value, attr, default)
    return value

def export_to_csv(
    django_model,
    write_to,
    exclude_fields = [],
    include_fields = [],
    ordering = [],
    keep_include_fields = True,
    show_others = True,
    fk_fields = {
      # 'fk_field_name_in_model': ['referenced_model_field_names']
    },
    write_header_row=True,
    records=None
    ):
  model_fields = get_field_names_from_model(django_model)
  writer = csv.writer(write_to)

  # mantain field order
  field_order = list(ordering) # provided order
  for field in include_fields: # include_field order
    if field not in field_order:
      field_order.append(field)
  for field in model_fields: # django model's order
    if field not in field_order:
      field_order.append(field)
  
  # build header
  header = []
  columns = []
  for field in field_order:
    # skip if field is pk_field
    if not is_includeable(field, include_fields, exclude_fields, keep_include_fields, show_others):
      continue
    
    # hanlde foreign key field
    if field in fk_fields:
      nested_model:Model = get_nested_attr(django_model, f'{field}.field.related_model')
      nested_fileds = fk_fields[field]
      
      if nested_fileds == "all":
        django_fileds = nested_model._meta.get_fields()
        nested_fileds = []
        for dj_filed in django_fileds:
          nested_fileds.append(dj_filed.name)

      for nested_field in nested_fileds:
        nested_header_name = get_header_name_from_field_name(nested_model, nested_field)
        nested_column_name = f'{field}.{nested_field}'
        header.append(f"{nested_model.__name__} - {nested_header_name}")
        columns.append(nested_column_name)
      continue

    header_name = get_header_name_from_field_name(django_model, field)
    column_name = field
    header.append(header_name)
    columns.append(column_name)

  # write header row
  if write_header_row:
    writer.writerow(header)
  del(header)

  if records is None:
    records = django_model.objects.all()
  for record in records:
    row = []
    for column in columns:
      value = get_nested_attr(record, column, '')
      row.append(value)
    # write record
    writer.writerow(row)
  del(records)
  del(writer)
  