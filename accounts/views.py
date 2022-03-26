import json
from django.http import Http404
from django.http.request import HttpRequest

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

# Models
from companies.models import SelfassesmentAccountSubmission
from .models import SelfemploymentIncomeSources, SelfemploymentExpenseSources, SelfemploymentDeductionSources, Months, SelfemploymentExpensesPerTaxYear, SelfemploymentIncomesPerTaxYear, SelfemploymentDeductionsPerTaxYear

# Serializers
from rest_framework.renderers import JSONRenderer
from .serializers import SelfemploymentIncomeSourcesSerializer, SelfemploymentExpenseSourcesSerializer, SelfemploymentDeductionSourcesSerializer, MonthsSerializer, SelfemploymentIncomesPerTaxYearSerializer, SelfemploymentExpensesPerTaxYearSerializer, SelfemploymentDeductionsPerTaxYearSerializer
dump_to_json = JSONRenderer()

from companies.views import URLS, serialized
from companies.decorators import allowed_for_staff, allowed_for_superuser


def get_object_or_None(model, *args, pk=None, **kwargs):
    try:
        if pk is not None:
            record = model.objects.get(pk=pk)
        else:
            record = model.objects.filter(*args, **kwargs).order_by('pk')
            if type(record) is QuerySet and len(record)>1:
                for rec in record[1:]:
                    rec.delete()
            if record:
                record = record[0]
            if type(record) is QuerySet and len(record) is 0:
                return None
        return record
    except ObjectDoesNotExist:
        return None


@login_required
@allowed_for_staff()
def index(request):
    context = {**URLS}
    return render(request, "accounts/index.html", context)


##############################################################################
## Views to update and insert data for incomes and expenses
##############################################################################
@csrf_exempt
@login_required
def upsert_expese_for_submission(request:HttpRequest, submission_id, month_id, expense_id):
    if not request.method == "POST":
        return Http404()
    
    try:
        loaded_data = json.loads(request.body.decode())
    except json.decoder.JSONDecodeError:
        return HttpResponse(json.dumps({'error': f'only json data is allowed'}), status=400)

    amount = loaded_data.get("amount", None)
    personal_usage_percentage = loaded_data.get("personal_usage_percentage", None)
    
    if amount is None and personal_usage_percentage is None:
        return HttpResponse(json.dumps({'error': f'amount or personal_usage is required'}), status=400)
    
    if personal_usage_percentage is not None and not 0<=personal_usage_percentage<=100:
        return HttpResponse(json.dumps({'error': f'personal_usage value should be between 0 and 100!'}), status=400)

    # retrive selfassemsent account submission record
    client = get_object_or_None(SelfassesmentAccountSubmission, pk=submission_id)
    if client is None:
        return HttpResponse(json.dumps({'error': f'SelfassesmentAccountSubmission with pk={submission_id} does not exist'}), status=404)
    
    # retrive month 
    month = get_object_or_None(Months, pk=month_id)
    if month is None:
        return HttpResponse(json.dumps({'error': f'Month with pk={month_id} does not exist'}), status=404)
    
    # retrive expense source
    expense = get_object_or_None(SelfemploymentExpenseSources, pk=expense_id)
    if expense is None:
        return HttpResponse(json.dumps({'error': f'Expense with pk={expense_id} does not exist'}), status=404)

    # Try to retrive ExpensesPerTaxYear if does not exist create it
    expense_for_tax_year = get_object_or_None(SelfemploymentExpensesPerTaxYear, client=client, month=month, expense_source=expense)

    # Update existing record 
    if expense_for_tax_year is not None:
        if amount is not None:
            expense_for_tax_year.amount = amount
        if personal_usage_percentage is not None:
            expense_for_tax_year.personal_usage_percentage = personal_usage_percentage
        expense_for_tax_year.save()
        return HttpResponse(json.dumps({'success': 'Updated existing record'}))
    
    # Save new record
    expense_for_tax_year = SelfemploymentExpensesPerTaxYear(
        expense_source=expense,
        client=client,
        month=month,
        )
    if amount is not None:
        expense_for_tax_year.amount = amount
    if personal_usage_percentage is not None:
        expense_for_tax_year.personal_usage_percentage = personal_usage_percentage
    expense_for_tax_year.save()
    return HttpResponse(json.dumps({'success': 'Updated existing record'}), status=201)

@csrf_exempt
@login_required
def upsert_income_for_submission(request, submission_id, month_id, income_id):
    if not request.method == "POST":
        raise Http404()
    
    try:
        loaded_data = json.loads(request.body.decode())
    except json.decoder.JSONDecodeError:
        return HttpResponse(json.dumps({'error': f'only json data is allowed'}), status=400)
    
    amount = loaded_data.get("amount", None)
    comission = loaded_data.get("comission", None)

    if amount is None and comission is None:
        return HttpResponse(json.dumps({'error': f'amount or comission must be specified'}), status=400)

    # retrive selfassemsent account submission record
    client = get_object_or_None(SelfassesmentAccountSubmission, pk=submission_id)
    if client is None:
        return HttpResponse(json.dumps({'error': f'SelfassesmentAccountSubmission with pk={submission_id} does not exist'}), status=404)
    
    # retrive month 
    month = get_object_or_None(Months, pk=month_id)
    if month is None:
        return HttpResponse(json.dumps({'error': f'Month with pk={month_id} does not exist'}), status=404)
    
    # retrive income source
    income = get_object_or_None(SelfemploymentIncomeSources, pk=income_id)
    if income is None:
        return HttpResponse(json.dumps({'error': f'IncomeSource with pk={income_id} does not exist'}), status=404)
    
    # Try to retrive IncomesPerTaxYear if does not exist create it
    income_for_tax_year = get_object_or_None(SelfemploymentIncomesPerTaxYear, client=client, month=month, income_source=income)
    
    # Update existing record 
    if income_for_tax_year:
        if amount is not None:
            income_for_tax_year.amount = amount
        if comission is not None:
            income_for_tax_year.comission = comission
        income_for_tax_year.save()
        return HttpResponse(json.dumps({'success': 'Updated existing record'}))
    
    # Save new record
    income_for_tax_year = SelfemploymentIncomesPerTaxYear(
        income_source=income,
        client=client,
        month=month,
        )
    if amount is not None:
        income_for_tax_year.amount = amount
    if comission is not None:
        income_for_tax_year.comission = comission
    income_for_tax_year.save()

    return HttpResponse(json.dumps({'success': 'Created new record'}), status=201)


@csrf_exempt
@login_required
def upsert_deduction_for_submission(request, submission_id, deduction_id):
    if not request.method == "POST":
        raise Http404()
    
    try:
        loaded_data = json.loads(request.body.decode())
    except json.decoder.JSONDecodeError:
        return HttpResponse(json.dumps({'error': f'only json data is allowed'}), status=400)
    
    amount = loaded_data.get("amount", None)
    allowance_percentage = loaded_data.get("allowance_percentage", None)
    personal_usage_percentage = loaded_data.get("personal_usage_percentage", None)

    if amount is None and allowance_percentage is None and personal_usage_percentage is None:
        return HttpResponse(json.dumps({'error': f'amount or allowance_percentage or personal_usage_percentage must be specified'}), status=400)
    
    if allowance_percentage and not 0<=allowance_percentage<=100:
        return HttpResponse(json.dumps({'error': f'allowance_percentage must be between 0 and 100!'}), status=400)
    if personal_usage_percentage and not 0<=personal_usage_percentage<=100:
        return HttpResponse(json.dumps({'error': f'personal_usage_percentage must be between 0 and 100!'}), status=400)

    # retrive selfassemsent account submission record
    client = get_object_or_None(SelfassesmentAccountSubmission, pk=submission_id)
    if client is None:
        return HttpResponse(json.dumps({'error': f'SelfassesmentAccountSubmission with pk={submission_id} does not exist'}), status=404)
    
    # retrive deduction source
    deduction_source = get_object_or_None(SelfemploymentDeductionSources, pk=deduction_id)
    if deduction_source is None:
        return HttpResponse(json.dumps({'error': f'DeductionSource with pk={deduction_id} does not exist'}), status=404)
    
    # Try to retrive IncomesPerTaxYear if does not exist create it
    deduction_for_tax_year = get_object_or_None(SelfemploymentDeductionsPerTaxYear, client=client, deduction_source=deduction_id)
    
    # Update existing record 
    if deduction_for_tax_year:
        if amount is not None:
            deduction_for_tax_year.amount = amount
        if allowance_percentage is not None:
            deduction_for_tax_year.allowance_percentage = allowance_percentage
        if personal_usage_percentage is not None:
            deduction_for_tax_year.personal_usage_percentage = personal_usage_percentage
        deduction_for_tax_year.save()
        return HttpResponse(json.dumps({'success': 'Updated existing record'}))
    
    # Save new record
    deduction_for_tax_year = SelfemploymentDeductionsPerTaxYear(
        client=client,
        deduction_source=deduction_source
    )
    if amount is not None:
        deduction_for_tax_year.amount = amount
    if allowance_percentage is not None:
        deduction_for_tax_year.allowance_percentage = allowance_percentage
    if personal_usage_percentage is not None:
        deduction_for_tax_year.personal_usage_percentage = personal_usage_percentage
    deduction_for_tax_year.save()

    return HttpResponse(json.dumps({'success': 'Created new record'}), status=201)


##############################################################################
## Views to return data for incomes and expenses tab
##############################################################################
@login_required
def get_expenses_for_submission(request: HttpRequest, submission_id):
    submission_expenses = SelfemploymentExpensesPerTaxYear.objects.filter(client=submission_id).order_by('expense_source', 'month__month_index')
    serialized_data = SelfemploymentExpensesPerTaxYearSerializer(submission_expenses, many=True)
    json_response = dump_to_json.render(serialized_data.data)
    return HttpResponse(json_response, content_type='application/json')

@login_required
def get_incomes_for_submission(request: HttpRequest, submission_id):
    submission_incomes = SelfemploymentIncomesPerTaxYear.objects.filter(client=submission_id).order_by('income_source', 'month__month_index')
    serialized_data = SelfemploymentIncomesPerTaxYearSerializer(submission_incomes, many=True)
    json_response = dump_to_json.render(serialized_data.data)
    return HttpResponse(json_response, content_type='application/json')

@login_required
def get_deductions_for_submission(request: HttpRequest, submission_id):
    submission_deductions = SelfemploymentDeductionsPerTaxYear.objects.filter(client=submission_id).order_by('deduction_source')
    serialized_data = SelfemploymentDeductionsPerTaxYearSerializer(submission_deductions, many=True)
    json_response = dump_to_json.render(serialized_data.data)
    return HttpResponse(json_response, content_type='application/json')


##############################################################################
## Views to return data for incomes and expenses tab
##############################################################################
@login_required
def get_all_expense_sources(request):
    expese_sources = SelfemploymentExpenseSources.objects.all()
    serialized = SelfemploymentExpenseSourcesSerializer(expese_sources, many=True)
    json_response = dump_to_json.render(serialized.data)
    return HttpResponse(json_response, content_type='application/json')

@login_required
def get_all_income_sources(request):
    income_sources = SelfemploymentIncomeSources.objects.all()
    serialized = SelfemploymentIncomeSourcesSerializer(income_sources, many=True)
    json_response = dump_to_json.render(serialized.data)
    return HttpResponse(json_response, content_type='application/json')

@login_required
def get_all_months(request):
    income_sources = Months.objects.all()
    serialized = MonthsSerializer(income_sources, many=True)
    json_response = dump_to_json.render(serialized.data)
    return HttpResponse(json_response, content_type='application/json')

@login_required
def get_all_deduction_sources(request):
    deduction_sources = SelfemploymentDeductionSources.objects.all()
    serialized = SelfemploymentDeductionSourcesSerializer(deduction_sources, many=True)
    json_response = dump_to_json.render(serialized.data)
    return HttpResponse(json_response, content_type='application/json')
