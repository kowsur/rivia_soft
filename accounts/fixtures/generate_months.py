import json
import calendar
import string
from textwrap import indent

STARTING_MONTH = 4
months = calendar.month_name

def yaml_month_format(pk, name, model="accounts.Months"):
    row = f"""- model: {model}
  pk: {pk}
  fields: 
    month_name: {name}
"""
    return row

def index_sequence_generator(starting_number=1, increment_by=1):
    while True:
        yield starting_number
        starting_number+=increment_by


def get_yaml_months():
    yaml_months = ""
    for i in range(STARTING_MONTH, 13):
        month = months[i]
        yaml_months += yaml_month_format(i, month)

    for i in range(1, STARTING_MONTH):
        month = months[i]
        yaml_months += yaml_month_format(i, month)
    return yaml_months


def get_json_month_obj(pk, month, index, model="accounts.Months"):
    month = {
            "model": model,
            "pk": pk,
            "fields": {
                "month_name": month,
                "month_index": index
            }
        }
    return month

def get_json_months():
    index_numbers = index_sequence_generator()
    json_months = []
    for i in range(STARTING_MONTH, 13):
        month = months[i]
        json_months.append(get_json_month_obj(i, month, next(index_numbers)))

    for i in range(1, STARTING_MONTH):
        month = months[i]
        json_months.append(get_json_month_obj(i, month, next(index_numbers)))
    
    return json.dumps(json_months, indent=4)



# print(get_yaml_months())
print(get_json_months())