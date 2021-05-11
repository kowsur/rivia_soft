from .html_generator import get_header_name_from_field_name, get_field_names_from_model, is_includeable
import csv


def export_to_csv(
    django_model,
    write_to,
    exclude_fields = [],
    include_fields = [],
    ordering = [],
    keep_include_fields = True,
    show_others = True,
    fk_fields = []
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
    col_name = get_header_name_from_field_name(django_model, field)
    header.append(col_name)
    columns.append(field)
  # write header row
  writer.writerow(header)
  del(header)

  records = django_model.objects.all()
  for record in records:
    row = []
    for column in columns:
      value = getattr(record, column, '')
      row.append(value)
    # write record
    writer.writerow(row)
  del(records)
  del(writer)
  