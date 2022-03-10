from webbrowser import get
from django.urls import path

from .views import index, get_all_expense_sources, get_all_income_sources, get_all_months, upsert_expese_for_submission, upsert_income_for_submission



urlpatterns = [
    path("", index),
    
    # update or set data
    path("set_income/<int:submission_id>/<int:month_id>/<int:income_id>/", upsert_income_for_submission),
    path("set_expense/<int:submission_id>/<int:month_id>/<int:expense_id>/", upsert_expese_for_submission),

    # get data
    path("expense_sources/", get_all_expense_sources),
    path("income_sources/", get_all_income_sources),
    path("months/", get_all_months),
]
