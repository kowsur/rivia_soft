import json
import calendar
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

def get_yaml_months():
    yaml_months = ""
    for i in range(STARTING_MONTH, 13):
        month = months[i]
        yaml_months += yaml_month_format(i, month)

    for i in range(1, STARTING_MONTH):
        month = months[i]
        yaml_months += yaml_month_format(i, month)
    return yaml_months


def get_json_month_obj(pk, month, model="accounts.Months"):
    month = {
            "model": model,
            "pk": pk,
            "fields": {
                "month_name": month
            }
        }
    return month

def get_json_months():
    json_months = []
    for i in range(STARTING_MONTH, 13):
        month = months[i]
        json_months.append(get_json_month_obj(i, month))

    for i in range(1, STARTING_MONTH):
        month = months[i]
        json_months.append(get_json_month_obj(i, month))
    
    return json.dumps(json_months, indent=4)



# print(get_yaml_months())
print(get_json_months())