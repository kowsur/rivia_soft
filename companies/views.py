from datetime import timedelta
from dateutil.relativedelta import relativedelta

import json
from django.http.response import Http404, HttpResponse
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls.exceptions import NoReverseMatch
from django.db.models import DurationField, F, ExpressionWrapper
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

#forms
from .forms import SelfassesmentCreationForm, SelfassesmentChangeForm, SelfassesmentDeleteForm
from .forms import SelfemploymentIncomeAndExpensesDataCollectionCreationForm, SelfemploymentIncomeAndExpensesDataCollectionUpdateForm, \
  SelfemploymentIncomeAndExpensesDataCollectionDeleteForm, SelfemploymentIncomeAndExpensesDataCollectionCreationFormForClients, \
  SelfemploymentIncomeAndExpensesDataCollectionAuthFormForClients
from .forms import SelfassesmentAccountSubmissionCreationForm, SelfassesmentAccountSubmissionChangeForm, SelfassesmentAccountSubmissionDeleteForm
from .forms import Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form
from .forms import SelfassesmentTrackerCreationForm, SelfassesmentTrackerChangeForm, SelfassesmentTrackerDeleteForm

from .forms import LimitedCreationForm, LimitedChangeForm, LimitedDeleteForm
from .forms import LimitedTrackerCreationForm, LimitedTrackerChangeForm, LimitedTrackerDeleteForm
from .forms import MergedTrackerCreateionForm
from .forms import LimitedSubmissionDeadlineTrackerCreationForm, LimitedSubmissionDeadlineTrackerChangeForm, LimitedSubmissionDeadlineTrackerDeleteForm
from .forms import LimitedVATTrackerCreationForm, LimitedVATTrackerChangeForm, LimitedVATTrackerDeleteForm
from .forms import LimitedConfirmationStatementTrackerCreationForm, LimitedConfirmationStatementTrackerChangeForm, LimitedConfirmationStatementTrackerDeleteForm

#models
from .models import  Selfassesment, SelfassesmentTracker, SelfassesmentAccountSubmission, SelfassesmentAccountSubmissionTaxYear, SelfemploymentIncomeAndExpensesDataCollection
from .models import Limited, LimitedTracker, LimitedSubmissionDeadlineTracker, LimitedVATTracker, LimitedConfirmationStatementTracker
from .models import AutoCreatedSelfassesmentTracker

# Serializers
from rest_framework.renderers import JSONRenderer
from .serializers import SelfassesmentAccountSubmissionSerializer
dump_model_to_json = JSONRenderer()

#export
from .export_models import export_to_csv

#queries
from .queries import db_search_Selfassesment, db_all_Selfassesment
from .queries import db_search_SelfemploymentIncomeAndExpensesDataCollection, db_all_SelfemploymentIncomeAndExpensesDataCollection
from .queries import db_search_SelfassesmentAccountSubmissionTaxYear, db_all_SelfassesmentAccountSubmissionTaxYear
from .queries import db_search_SelfassesmentAccountSubmission, db_all_SelfassesmentAccountSubmission
from .queries import db_search_SelfassesmentTracker, db_all_SelfassesmentTracker

from .queries import db_all_Limited, db_search_Limited
from .queries import db_search_LimitedTracker, db_all_LimitedTracker
from .queries import db_search_LimitedSubmissionDeadlineTracker, db_all_LimitedSubmissionDeadlineTracker
from .queries import db_search_LimitedVATTracker, db_all_LimitedVATTracker
from .queries import db_search_LimitedConfirmationStatementTracker, db_all_LimitedConfirmationStatementTracker

# serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer, SelfassesmentAccountSubmissionTaxYearSerializer, SelfassesmentSerializer, LimitedSerializer

#permissions
from .decorators import allowed_for_staff, allowed_for_superuser


from .url_variables import APPLICATION_NAME, URL_NAMES, URL_PATHS, Full_URL_PATHS_WITHOUT_ARGUMENTS, URL_NAMES_PREFIXED_WITH_APP_NAME
from .url_variables import *

# html generator
from .html_generator import get_field_names_from_model, generate_template_tag_for_model, generate_data_container_table
from .repr_formats import HTML_Generator, Forms as FK_Formats

application_name = APPLICATION_NAME
# these path names will be passed to templates to use in the navbar links
URLS = {
  'home': f'{application_name}:home',

  **Full_URL_PATHS_WITHOUT_ARGUMENTS.get_dict(),
  **URL_NAMES_PREFIXED_WITH_APP_NAME.get_dict()
}
user_details_url_without_argument = '/u/details/'

from pprint import pp


SELFASSESMENT_FK_FIELDS_FOR_EXPORT = 'all' #['client_name', 'client_file_number', 'HMRC_referance', 'personal_post_code']
LIMITED_FK_FIELDS_FOR_EXPORT = 'all' #['client_name', 'client_file_number', 'director_phone_number', 'director_post_code']
# =============================================================================================================
# =============================================================================================================
# Selfassesment
@login_required
def home_selfassesment(request):
  pk_field = 'client_id'
  exclude_fields = []
  include_fields = ['client_file_number', 'client_name', 'is_active', 'incomplete_tasks', 'personal_phone_number', 'personal_email', 'UTR', 'NINO', 'HMRC_agent', "created_by", "date_of_registration"]
  keep_include_fields = True
  show_others = False
  model_fields = get_field_names_from_model(Selfassesment)
  model_fields.append('incomplete_tasks')
  context = {
    **URLS,
    'caption': 'View Selfassesment',
    'page_title': 'View Selfassesment',
    
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_create_name,
    'export_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_export_name,

    'template_tag': generate_template_tag_for_model(Selfassesment, pk_field=pk_field, show_id=False, exclude_fields=exclude_fields, include_fields=include_fields, keep_include_fields=keep_include_fields, show_others=show_others),
    'data_container': generate_data_container_table(Selfassesment, pk_field=pk_field, show_id=False, exclude_fields=exclude_fields, include_fields=include_fields, keep_include_fields=keep_include_fields, show_others=show_others),

    'frontend_data':{
      'all_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_viewall_url,
      'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_search_url,
      'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_update_url,
      'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_delete_url,  
      'model_fields': model_fields
    },
  }
  return render(request=request, template_name='companies/home.html', context=context)

@login_required
def view_selfassesment(request):
  return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_home_name)

@login_required
def create_selfassesment(request):
  context = {
    **URLS,
    'page_title': 'Create Selfassesment',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_home_name,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_create_name,
    'form_title': 'Selfassesment Account Year Assign Form',
    'form': SelfassesmentCreationForm(initial={'client_file_number': Selfassesment.get_next_file_number()})
  }

  if request.method == 'POST':
    form = SelfassesmentCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.set_defaults()
      assesment.created_by = request.user
      assesment.save()
      
      job_description = 'Issues\n'

      if not assesment.UTR:
        # Create Tracker
        tracker = SelfassesmentTracker()
        tracker.client_id = assesment
        tracker.deadline = timezone.now()+timedelta(2)
        tracker.has_issue = True
        tracker.new_customer = True
        tracker.job_description = job_description + '    - Apply/ask for UTR\n'
        tracker.save()
        messages.success(request, f"New Selfassesment Tracker has been created for {assesment} because it doesn't have UTR!")

        # Save reference
        reference = AutoCreatedSelfassesmentTracker(
          selfassesment = assesment,
          selfassesment_tracker = tracker,
          reference = AutoCreatedSelfassesmentTracker.CreatedForField.UTR)
        reference.save()

      if not assesment.NINO:
        # Create Tracker
        tracker = SelfassesmentTracker()
        tracker.client_id = assesment
        tracker.deadline = timezone.now()+timedelta(2)
        tracker.has_issue = True
        tracker.new_customer = True
        tracker.job_description = job_description + '    - Ask for NINO\n'
        tracker.save()
        messages.success(request, f"New Selfassesment Tracker has been created for {assesment} because it doesn't have NINO!")

        # Save reference
        reference = AutoCreatedSelfassesmentTracker(
          selfassesment = assesment,
          selfassesment_tracker = tracker,
          reference = AutoCreatedSelfassesmentTracker.CreatedForField.NINO)
        reference.save()

      if not assesment.HMRC_agent:
        # Create Tracker
        tracker = SelfassesmentTracker()
        tracker.client_id = assesment
        tracker.deadline = timezone.now()+timedelta(2)
        tracker.has_issue = True
        tracker.new_customer = True
        tracker.job_description = job_description + '    - Apply for agent\n'
        tracker.save()
        messages.success(request, f"New Selfassesment Tracker has been created for {assesment} because HMRC agent is inactive!")
        
        # Save reference
        reference = AutoCreatedSelfassesmentTracker(
          selfassesment = assesment,
          selfassesment_tracker = tracker,
          reference = AutoCreatedSelfassesmentTracker.CreatedForField.HMRC_AGENT)
        reference.save()

      context['form'] = SelfassesmentCreationForm(initial={'client_file_number': Selfassesment.get_next_file_number()})
  return render(request, template_name='companies/create.html', context=context)

@login_required
def get_details_selfassesment(request, client_id=None):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    record = get_object_or_404(Selfassesment, client_id=client_id)
    response = SelfassesmentSerializer(instance=record).data
    return HttpResponse(json.dumps(response))
  raise Http404

def mark_tracker_complete(tracker:SelfassesmentTracker)->None:
  tracker.is_completed = True
  tracker.has_issue = False
  tracker.save()

@login_required
def update_selfassesment(request, client_id:int):
  context = {
    **URLS,
    'page_title': f'Update Selfassesment',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_home_name,
    'id': client_id,
    'update_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_update_name,
    'form_title': 'Selfassesment Update Form',
    'form': SelfassesmentChangeForm()
  }

  try:
    record =  Selfassesment.objects.get(client_id=client_id)
    context['form'] = SelfassesmentChangeForm(instance=record)
  except Selfassesment.DoesNotExist:
    messages.error(request, f'Selfassesment Account having id {client_id} does not exists!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_home_name)
    raise Http404

  if request.method == 'POST':
    form = SelfassesmentChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      # Update auto created trackers as compeleted
      if assesment.UTR:
        reference = AutoCreatedSelfassesmentTracker.objects.filter(
          selfassesment = assesment,
          reference = AutoCreatedSelfassesmentTracker.CreatedForField.UTR
          ).first()
        if reference:
          tracker = reference.selfassesment_tracker
          mark_tracker_complete(tracker)
          reference.delete()

      if assesment.NINO:
        reference = AutoCreatedSelfassesmentTracker.objects.filter(
          selfassesment = assesment,
          reference = AutoCreatedSelfassesmentTracker.CreatedForField.NINO
          ).first()
        if reference:
          tracker = reference.selfassesment_tracker
          mark_tracker_complete(tracker)
          reference.delete()

      if assesment.HMRC_agent:
        reference = AutoCreatedSelfassesmentTracker.objects.filter(
          selfassesment = assesment,
          reference = AutoCreatedSelfassesmentTracker.CreatedForField.HMRC_AGENT
          ).first()
        if reference:
          tracker = reference.selfassesment_tracker
          mark_tracker_complete(tracker)
          reference.delete()
      
      messages.success(request, f'Selfassesment has been updated having id {client_id}!')
    else:
      messages.error(request, f'Updating Selfassesment {client_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_home_name)
def delete_selfassesment(request, client_id:int):
  context = {
    **URLS,
    'page_title': 'Delete Selfassesment',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_home_name,
    'id': client_id,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_delete_name,
    'form_title': "Selfassesment Delete Form",
    'form': SelfassesmentDeleteForm()
  }
  try:
    record =  Selfassesment.objects.get(client_id=client_id)
  except Selfassesment.DoesNotExist:
    messages.error(request, f'Selfassesment record with id {client_id}, you are looking for does not exist!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_home_name)

  if request.method == 'POST':
    form = SelfassesmentDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Selfassesment has been deleted having id {client_id}!')
    else:
      messages.error(request, f'Selfassesment deletion of id {client_id} failed!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_home_name)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_selfassesment(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    search_text = request.GET.get('q', '')
    if search_text.strip()=='':
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_viewall_name)
    records = db_search_Selfassesment(search_text, limit)
    records = records.order_by("-client_file_number")
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_selfassesment(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_Selfassesment(limit)
    records = records.order_by("-client_file_number")
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def export_selfassesment(request):
  response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': f'attachment; filename="selfassesment_{timezone.localtime()}.csv"'},
  )
  include_fields = ['is_active', 'client_file_number', 'client_name', 'personal_phone_number', 'personal_email', 'UTR', 'NINO', 'HMRC_agent']
  exclude_fields = []
  keep_include_fields = True
  show_others = True
  export_to_csv(
    django_model = Selfassesment,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others
    )
  return response

@api_view(['GET'])
def serialized(request):
  
  return SelfassesmentSerializer()



# =============================================================================================================
# =============================================================================================================
# SelfassesmentAccountSubmissionTaxYear

@login_required
def get_details_selfassesment_account_submission_tax_year(request, id=None):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    record = get_object_or_404(SelfassesmentAccountSubmissionTaxYear, id=id)
    response = SelfassesmentAccountSubmissionTaxYearSerializer(instance=record).data
    return HttpResponse(json.dumps(response))
  raise Http404

@login_required
def search_selfassesment_account_submission_tax_year(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    search_text = request.GET.get('q', '')
    if search_text.strip()=='':
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_viewall_name)
    records = db_search_SelfassesmentAccountSubmissionTaxYear(search_text, limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_selfassesment_account_submission_tax_year(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_SelfassesmentAccountSubmissionTaxYear(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404


# =============================================================================================================
# =============================================================================================================
# SelfemploymentIncomeAndExpensesDataCollection
@login_required
def home_selfassesment_data_collection(request):
  pk_field = 'id'
  exclude_fields = []
  include_fields = ['selfassesment', 'tax_year', 'is_submitted']
  keep_include_fields = True
  show_others = True
  model_fields = get_field_names_from_model(SelfemploymentIncomeAndExpensesDataCollection)
  context = {
    **URLS,
    'caption': 'View Selfassesment Data Collection',
    'page_title': 'View Selfassesment Data Collection',
    
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_create_name,
    'export_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_export_name,

    'template_tag': generate_template_tag_for_model(SelfemploymentIncomeAndExpensesDataCollection, pk_field=pk_field, show_id=False, exclude_fields=exclude_fields, include_fields=include_fields, keep_include_fields=keep_include_fields, show_others=show_others),
    'data_container': generate_data_container_table(SelfemploymentIncomeAndExpensesDataCollection, pk_field=pk_field, show_id=False, exclude_fields=exclude_fields, include_fields=include_fields, keep_include_fields=keep_include_fields, show_others=show_others),

    'frontend_data':{
      'all_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Data_Collection_viewall_url,
      'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Data_Collection_search_url,
      'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Data_Collection_update_url,
      'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Data_Collection_delete_url,
      'model_fields': model_fields
    },
  }
  return render(request=request, template_name='companies/home.html', context=context)


def create_selfassesment_data_collection_for_client(request, selfassesment=None):
  if not selfassesment and request.method!='POST':
    raise Http404
  
  context = {
    'page_title': 'Submit Income and Expense Data',
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_create_name_for_client,
    'form_title': 'Submit Income And Expense Data',
    'form': SelfemploymentIncomeAndExpensesDataCollectionCreationFormForClients(initial={
      'selfassesment': selfassesment,
      'tax_year': SelfassesmentAccountSubmissionTaxYear.get_max_year()
    })
  }

  if request.method == 'POST':
    form = SelfemploymentIncomeAndExpensesDataCollectionCreationFormForClients(request.POST)
    context['form'] = form

    try:
      tax_year = form.data.get('tax_year', None)
      tax_year = SelfassesmentAccountSubmissionTaxYear.objects.get(pk=tax_year)
    except SelfassesmentAccountSubmissionTaxYear.DoesNotExist:
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_auth_name_for_client)
    
    try:
      selfassesment = form.data.get('selfassesment', None)
      selfassesment = Selfassesment.objects.get(pk=selfassesment)
    except Selfassesment.DoesNotExist:
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_auth_name_for_client)
    
    if form.is_valid() and tax_year and selfassesment:
      assesment = form.save(commit=False)
      assesment.tax_year = tax_year
      assesment.selfassesment = selfassesment
      assesment.save()
      messages.add_message(request, messages.SUCCESS, 'We recieved your data!')
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_auth_name_for_client)
    else:
      messages.error(request, f'Action failed due to invalid data!')
  return render(request, template_name='companies/create_without_auth.html', context=context)

def auth_selfassesment_data_collection_for_client(request):
  context = {
    'page_title': 'Auth Income and Expense Data collection',
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_auth_name_for_client,
    'form_title': 'Auth Income And Expense Data Collection',
    'form': SelfemploymentIncomeAndExpensesDataCollectionAuthFormForClients()
  }
  if request.method=="POST":
    form = SelfemploymentIncomeAndExpensesDataCollectionAuthFormForClients(request.POST)
    context['form'] = form
    if form.is_valid():
      utr = form.cleaned_data.get('utr')
      try:
        selfassesment = Selfassesment.objects.get(UTR=utr)
        context = {
          'page_title': 'Submit Income and Expense Data',
          'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_create_name_for_client,
          'form_title': 'Submit Income And Expense Data',
          'form': SelfemploymentIncomeAndExpensesDataCollectionCreationFormForClients(initial={
            'selfassesment': selfassesment,
            'tax_year': SelfassesmentAccountSubmissionTaxYear.get_max_year()
          })
        }
        # return redirect(to=URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_create_name_for_client, selfassesment=selfassesment)
        return render(request, template_name='companies/create_without_auth.html', context=context)
      except Selfassesment.DoesNotExist:
        form.add_error('utr', 'Invalid UTR')
  return render(request, template_name='companies/create_without_auth.html', context=context)

@login_required
def create_selfassesment_data_collection(request):
  context = {
    **URLS,

    'page_title': 'Create Selfassesment Income and Expense data',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_home_name,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_create_name,
    'form_title': 'Selfassesment Income And Expense Data Collection',
    'form': SelfemploymentIncomeAndExpensesDataCollectionCreationForm(initial={
      'selfassesment': None,
      'tax_year': SelfassesmentAccountSubmissionTaxYear.get_max_year()}
      )
  }

  if request.method == 'POST':
    form = SelfemploymentIncomeAndExpensesDataCollectionCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.save()
    else:
      messages.error(request, f'Action failed due to invalid data!')
  return render(request, template_name='companies/create.html', context=context)

@login_required
def update_selfassesment_data_collection(request, data_id):
  context = {
    **URLS,
    'page_title': f'Update Collected Data',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_home_name,
    'id': data_id,
    'update_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_update_name,
    'form_title': 'Update Collected Data Form',
    'form': SelfemploymentIncomeAndExpensesDataCollectionUpdateForm()
  }

  try:
    record =  SelfemploymentIncomeAndExpensesDataCollection.objects.get(id=data_id)
    context['form'] = SelfemploymentIncomeAndExpensesDataCollectionUpdateForm(instance=record)
  except SelfemploymentIncomeAndExpensesDataCollection.DoesNotExist:
    messages.error(request, f'Collected Data having id {data_id} does not exists!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_home_name)
    raise Http404

  if request.method == 'POST':
    form = SelfemploymentIncomeAndExpensesDataCollectionUpdateForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      collected_data = form.save()
      collected_data.save()
      messages.success(request, f'Collected Data has been updated having id {data_id}!')
    else:
      messages.error(request, f'Updating Collected Data having id {data_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_update_name)
def delete_selfassesment_data_collection(request, data_id:int):
  context = {
    **URLS,
    'page_title': 'Selfassesment Income And Expense Data Collection Deletion',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_viewall_name,
    'id': data_id,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_delete_name,
    'form_title': "Selfassesment Income And Expense Data Delete Form",
    'form': SelfemploymentIncomeAndExpensesDataCollectionDeleteForm()
  }
  try:
    record =  SelfemploymentIncomeAndExpensesDataCollection.objects.get(id=data_id)
  except SelfemploymentIncomeAndExpensesDataCollection.DoesNotExist:
    messages.error(request, f'Selfassesment Collected Data record with id {data_id}, you are looking for does not exist!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_home_name)

  if request.method == 'POST':
    form = SelfemploymentIncomeAndExpensesDataCollectionDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Selfassesment Collected Data has been deleted having id {data_id}!')
    else:
      messages.error(request, f'Selfassesment Collected Data deletion of id {data_id} failed!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_home_name)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_selfassesment_data_collection(request, limit:int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    search_text = request.GET.get('q', '')
    if search_text.strip()=='':
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Data_Collection_viewall_name)
    records = db_search_SelfemploymentIncomeAndExpensesDataCollection(search_text, limit)
    records = records.order_by("-created_at")
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_selfassesment_data_collection(request, limit:int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_SelfemploymentIncomeAndExpensesDataCollection(limit)
    records = records.order_by("-created_at")
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def export_selfassesment_data_collection(request):
  response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': f'attachment; filename="selfassesment_{timezone.localtime()}.csv"'},
  )
  include_fields = []
  exclude_fields = []
  fk_fields = {
    'selfassesment': 'all',
    'tax_year': ['tax_year']
  }
  keep_include_fields = True
  show_others = True
  export_to_csv(
    django_model = SelfemploymentIncomeAndExpensesDataCollection,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others,
    fk_fields=fk_fields
    )
  return response



# =============================================================================================================
# =============================================================================================================
# SelfassesmentAccountSubmission
def get_selfassesment_account_submissions_where_status_PAID():
  return SelfassesmentAccountSubmission.objects.filter(payment_status="PAID")

def get_selfassesment_account_submissions_where_status_NOT_PAID():
  return SelfassesmentAccountSubmission.objects.filter(payment_status="NOT PAID")

def get_selfassesment_account_submissions_where_status_REQUEST():
  return SelfassesmentAccountSubmission.objects.filter(status="REQUEST")

def get_selfassesment_account_submissions_where_status_PROCESSING():
  return SelfassesmentAccountSubmission.objects.filter(status="PROCESSING")

def get_selfassesment_account_submissions_where_status_BOOK_APPOINTMENT():
  return SelfassesmentAccountSubmission.objects.filter(status="BOOK APPOINTMENT")

def get_selfassesment_account_submissions_where_status_READY_FOR_SUBMIT():
  return SelfassesmentAccountSubmission.objects.filter(status="READY FOR SUBMIT")

def get_selfassesment_account_submissions_where_status_WAITING_FOR_CONFIRMATION():
  return SelfassesmentAccountSubmission.objects.filter(status="WAITING FOR CONFIRMATION")

def get_selfassesment_account_submissions_where_status_SUBMITTED():
  return SelfassesmentAccountSubmission.objects.filter(status="SUBMITTED")

def get_selfassesment_account_submissions_where_status_ASSIGNED_TO_ME(user):
  return SelfassesmentAccountSubmission.objects.filter(assigned_to=user)


@login_required
def home_selfassesment_account_submission(request):
  pk_field = 'submission_id'
  exclude_fields = []
  keep_include_fields = True
  context = {
    **URLS,
    'caption': 'View Selfassesment Account Submission',
    'page_title': 'View Selfassesment Account Submission',
    
    # 'add_all_url': URL_NAMES_PREFIXED_WITH_APP_NAME.add_all_Selfassesment_to_Selfassesment_Account_Submission_name,
    # 'add_all_text': 'Add all Selfassesment to Selfassesment Account Submission',

    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_create_name,
    'export_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_export_name,

    'template_tag': generate_template_tag_for_model(SelfassesmentAccountSubmission, pk_field=pk_field, show_id=True, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),
    'data_container': generate_data_container_table(SelfassesmentAccountSubmission, pk_field=pk_field, show_id=True, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),

    "counts": True,
    "selfassesment_account_submission_counts": True,
    "selfassesment_account_submission_status_PAID": get_selfassesment_account_submissions_where_status_PAID().count(),
    "selfassesment_account_submission_status_NOT_PAID": get_selfassesment_account_submissions_where_status_NOT_PAID().count(),
    "selfassesment_account_submission_status_REQUEST": get_selfassesment_account_submissions_where_status_REQUEST().count(),
    "selfassesment_account_submission_status_PROCESSING": get_selfassesment_account_submissions_where_status_PROCESSING().count(),
    "selfassesment_account_submission_status_BOOK_APPOINTMENT": get_selfassesment_account_submissions_where_status_BOOK_APPOINTMENT().count(),
    "selfassesment_account_submission_status_READY_FOR_SUBMIT": get_selfassesment_account_submissions_where_status_READY_FOR_SUBMIT().count(),
    "selfassesment_account_submission_status_WAITING_FOR_CONFIRMATION": get_selfassesment_account_submissions_where_status_WAITING_FOR_CONFIRMATION().count(),
    "selfassesment_account_submission_status_SUBMITTED": get_selfassesment_account_submissions_where_status_SUBMITTED().count(),
    "selfassesment_account_submission_status_ASSIGEND_TO_ME": get_selfassesment_account_submissions_where_status_ASSIGNED_TO_ME(request.user).count(),

    'frontend_data':{
      'all_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Account_Submission_viewall_url,
      'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Account_Submission_search_url,
      'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Account_Submission_update_url,
      'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Account_Submission_delete_url,  
      'model_fields': get_field_names_from_model(SelfassesmentAccountSubmission)
    },
  }
  return render(request=request, template_name='companies/home.html', context=context)

@login_required
def view_selfassesment_account_submission(request):
  return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name)

@login_required
def create_selfassesment_account_submission(request):
  context = {
    **URLS,

    'page_title': 'Create Selfassesment Account Submission',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_create_name,
    'form_title': 'Selfassesment Account Submission Creation Form',
    'form': SelfassesmentAccountSubmissionCreationForm(initial={'submitted_by': request.user.user_id, 'tax_year': SelfassesmentAccountSubmissionTaxYear.get_max_year()})
  }

  if request.method == 'POST':
    form = SelfassesmentAccountSubmissionCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      try:
        assesment = form.save()
        assesment.prepared_by = request.user
        assesment.set_defaults(request)
        assesment.save()
        messages.success(request, f'New Selfassesment Account Submission has been created with id {assesment.submission_id}!')
        context['form'] = SelfassesmentAccountSubmissionCreationForm(initial={'submitted_by': request.user.user_id})
      except IntegrityError:
        messages.error(request, f"Selfassesment Account Submission can't be updated because Client Name, Tax Year and Status is SUBMITTED is not unique!")
    else:
      messages.error(request, f'Action failed due to invalid data!')
  return render(request, template_name='companies/create.html', context=context)

@login_required
def update_selfassesment_account_submission(request, submission_id:int):
  context = {
    **URLS,
    'page_title': f'Update Selfassesment Account Submission',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name,
    'id': submission_id,
    'update_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_update_name,
    'form_title': 'Selfassesment Account Submission Update Form',
    'form': SelfassesmentAccountSubmissionChangeForm()
  }

  try:
    record =  SelfassesmentAccountSubmission.objects.get(submission_id=submission_id)
    context['form'] = SelfassesmentAccountSubmissionChangeForm(instance=record)
  except SelfassesmentAccountSubmission.DoesNotExist:
    messages.error(request, f'Selfassesment Account Submission having id {submission_id} does not exists!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name)
    raise Http404

  if request.method == 'POST':
    form = SelfassesmentAccountSubmissionChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      try:
        assesment = form.save(commit=False)
        assesment.set_defaults(request)
        assesment.save()
        messages.success(request, f'Selfassesment Account Submission has been updated having id {submission_id}!')
      except IntegrityError:
        messages.error(request, f"Selfassesment Account Submission can't be updated because Client Name, Tax Year and Status is SUBMITTED is not unique!")
    else:
      messages.error(request, f'Updating Selfassesment Account Submission having id {submission_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name)
def delete_selfassesment_account_submission(request, submission_id:int):
  context = {
    **URLS,
    'page_title': 'Delete Selfassesment Account Submission',
    'id': submission_id,
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_delete_name,
    'form_title': "Selfassesment Account Submission Delete Form",
    'form': SelfassesmentAccountSubmissionDeleteForm()
  }

  try:
    record = SelfassesmentAccountSubmission.objects.get(submission_id=submission_id)
  except SelfassesmentAccountSubmission.DoesNotExist:
    messages.error(request, f'Selfassesment Account Submission record with id {submission_id}, you are looking for does not exist!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name)
  
  if request.method == 'POST':
    form = SelfassesmentAccountSubmissionDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Selfassesment Account Submission has been deleted having id {submission_id}!')
    else:
      messages.error(request, f'Deletion of Selfassesment Account Submission having id {submission_id} failed!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_selfassesment_account_submission(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    search_text = request.GET.get('q', '')
    submission_id = request.GET.get('pk', None)
    
    if submission_id:
      error_message = {'error': 'The resource you are looking for does not exist'}
      error_response = HttpResponse(json.dumps(error_message), content_type='application/json', status=404)

      if not submission_id.isnumeric():
        return error_response

      try:
        submission_record = SelfassesmentAccountSubmission.objects.get(pk=submission_id)
      except SelfassesmentAccountSubmission.DoesNotExist:
        return error_response
      
      serialized_record = SelfassesmentAccountSubmissionSerializer(instance=submission_record)
      json_response = dump_model_to_json.render(serialized_record.data)
      return HttpResponse(json_response, content_type='application/json')


    # if tasks query paramter exists then return tasks
    if request.GET.get('tasks'):
      tasks = {
            "selfassesment_account_submission_status_PAID": get_selfassesment_account_submissions_where_status_PAID(),
            "selfassesment_account_submission_status_NOT_PAID": get_selfassesment_account_submissions_where_status_NOT_PAID(),
            "selfassesment_account_submission_status_REQUEST": get_selfassesment_account_submissions_where_status_REQUEST(),
            "selfassesment_account_submission_status_PROCESSING": get_selfassesment_account_submissions_where_status_PROCESSING(),
            "selfassesment_account_submission_status_BOOK_APPOINTMENT": get_selfassesment_account_submissions_where_status_BOOK_APPOINTMENT(),
            "selfassesment_account_submission_status_READY_FOR_SUBMIT": get_selfassesment_account_submissions_where_status_READY_FOR_SUBMIT(),
            "selfassesment_account_submission_status_WAITING_FOR_CONFIRMATION": get_selfassesment_account_submissions_where_status_WAITING_FOR_CONFIRMATION(),
            "selfassesment_account_submission_status_SUBMITTED": get_selfassesment_account_submissions_where_status_SUBMITTED(),
            "selfassesment_account_submission_status_ASSIGEND_TO_ME": get_selfassesment_account_submissions_where_status_ASSIGNED_TO_ME(request.user),
      }
      records = tasks.get(request.GET.get('tasks'), [])
      data = serialize(queryset=records, format='json')
      return HttpResponse(data, content_type='application/json')

    if search_text.strip()=='':
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_viewall_name)
    records = db_search_SelfassesmentAccountSubmission(search_text, limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_selfassesment_account_submission(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_SelfassesmentAccountSubmission(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def export_selfassesment_account_submission(request):
  response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': f'attachment; filename="selfassesment_account_submimssion_{timezone.localtime()}.csv"'},
  )
  include_fields = []
  exclude_fields = ['submission_id']
  fk_fields = {
    'client_id': 'all'
  }
  keep_include_fields = True
  show_others = True
  export_to_csv(
    django_model = SelfassesmentAccountSubmission,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others,
    fk_fields = fk_fields
    )
  return response

# add_all_selfassesment_to_selfassesment_account_submission_w_submission_year
@login_required
def add_all_selfassesment_to_selfassesment_account_submission_w_submission_year(request):
  context = {
    **URLS,
    'page_title': f'Add all Selfassesment to Selfassesment Account Submission',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.add_all_Selfassesment_to_Selfassesment_Account_Submission_name,
    'form_title': 'Add all Selfassesment to Selfassesment Account Submission',
    'form': Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form(initial={'submitted_by': request.user, 'account_prepared_by': request.user})
  }
  if not request.user.is_superuser:
    messages.error(request, 'Only Superusers can use this feature!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name)

  if request.method=='POST':
    form = Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form(data=request.POST)
    context['form'] = form
    if form.is_valid():
      submitted_by = form.cleaned_data.get('submitted_by')
      if submitted_by==None:
        form.cleaned_data['submitted_by'] = request.user

      all_Selfassesments = Selfassesment.objects.all()
      
      for assesment in all_Selfassesments:
        form.cleaned_data['client_id'] = assesment
        instance = SelfassesmentAccountSubmission(**form.cleaned_data)
        instance.set_defaults()
        if form.cleaned_data.get('prepared_by'):
          instance.prepared_by = form.cleaned_data.get('prepared_by')
        instance.save()
      messages.success(request, 'Added all Selfassesment to Selfassesment Account Submission!')
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name)
  return render(request, 'companies/create.html', context=context)


# =============================================================================================================
# =============================================================================================================
# SelfassesmentTracker
selfassesment_tracker_home_redirect_page = URL_NAMES_PREFIXED_WITH_APP_NAME.Merged_Tracker_home_name

def get_selfassesment_trackers_where_tasks_customers_are_new():
  return SelfassesmentTracker.objects.filter(new_customer=True, is_completed=False)

def get_selfassesment_trackers_where_future_tasks_are_incomplete():
  return SelfassesmentTracker.objects.filter(is_completed=False, deadline__gt=timezone.localtime())

def get_selfassesment_trackers_where_todays_tasks_are_incomplete():
  return SelfassesmentTracker.objects.filter(is_completed=False, deadline=timezone.localtime())

def get_selfassesment_trackers_where_previous_tasks_are_incomplete():
  return SelfassesmentTracker.objects.filter(deadline__lt=timezone.localtime(), is_completed=False)

def get_selfassesment_trackers_where_tasks_has_issues():
  return SelfassesmentTracker.objects.filter(has_issue=True)

def get_selfassesment_trackers_where_tasks_assigned_to_user(user):
  return SelfassesmentTracker.objects.filter(assigned_to=user, is_completed=False)

@login_required
def home_selfassesment_tracker(request):
  pk_field = 'tracker_id'
  exclude_fields = set(['tracker_id', 'is_updated'])
  include_fields = ['tracker_id', 'client_id', 'job_description', 'deadline', 'remarks','is_completed', 'has_issue', 'complete_date', 'done_by', 'created_by','creation_date', 'issue_created_by']

  keep_include_fields = True
  context = {
    **URLS,
    'page_title': 'View Selfassesment Tracker',
    'caption': 'View Selfassesment Tracker',

    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_create_name,
    'export_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_export_name,

    'counts': True,
    'tracker_task_counts': True,
    'new_customers': get_selfassesment_trackers_where_tasks_customers_are_new().count(),
    'future_incomplete_tasks': get_selfassesment_trackers_where_future_tasks_are_incomplete().count(),
    'todays_incomplete_tasks': get_selfassesment_trackers_where_todays_tasks_are_incomplete().count(),
    'previous_incomplete_tasks': get_selfassesment_trackers_where_previous_tasks_are_incomplete().count(),
    'task_has_issue': get_selfassesment_trackers_where_tasks_has_issues().count(),
    'my_tasks': get_selfassesment_trackers_where_tasks_assigned_to_user(request.user).count(),

    'template_tag': generate_template_tag_for_model(SelfassesmentTracker, pk_field=pk_field, show_id=True, include_fields=include_fields, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),
    'data_container': generate_data_container_table(SelfassesmentTracker, pk_field=pk_field, show_id=True, include_fields=include_fields, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),

    'frontend_data':{
      'all_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_viewall_url,
      'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_search_url,
      'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_update_url,
      'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_delete_url,  
      'model_fields': get_field_names_from_model(SelfassesmentTracker)
    },
  }
  return render(request=request, template_name='companies/home.html', context=context)

@login_required
def view_selfassesment_tracker(request):
  return redirect(selfassesment_tracker_home_redirect_page)

@login_required
def create_selfassesment_tracker(request):
  context = {
    **URLS,

    'page_title': 'Create Selfassesment Tracker',
    'view_url': selfassesment_tracker_home_redirect_page,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_create_name,
    'form_title': 'Selfassesment Tracker Creation Form',
    'form': SelfassesmentTrackerCreationForm(initial={'created_by': request.user.user_id})
  }
  redirect_to = None

  if request.method == 'POST':
    redirect_to = request.POST.get('redirect_to', None)
    form = SelfassesmentTrackerCreationForm(request.POST, initial={'created_by': request.user.user_id})
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.created_by = request.user
      if not assesment.issue_created_by and assesment.has_issue:
        assesment.issue_created_by = request.user
      assesment.save()
      messages.success(request, f'New Selfassesment Tracker has been created with id {assesment.tracker_id}!')
      context['form'] = SelfassesmentTrackerCreationForm(initial={'created_by': request.user.user_id})
  try:
    if not redirect_to:
      redirect_to = request.GET.get('redirect_to')
    if redirect_to:
      return redirect(redirect_to, permanent=True)
  except NoReverseMatch:
    raise Http404
  return render(request, template_name='companies/create.html', context=context)


@login_required
def update_selfassesment_tracker(request, tracker_id:int):
  context = {
    **URLS,
    'page_title': f'Update Selfassesment Tracker',
    'view_url': selfassesment_tracker_home_redirect_page,
    'id': tracker_id,
    'update_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_update_name,
    'form_title': 'Selfassesment Update Form',
    'form': SelfassesmentTrackerChangeForm()
  }

  try:
    record =  SelfassesmentTracker.objects.get(tracker_id=tracker_id)
    context['form'] = SelfassesmentTrackerChangeForm(instance=record)
    if record.is_completed:
      messages.error(request, message=f"Task {tracker_id} is completed therefore can't be updated!")
      return redirect(selfassesment_tracker_home_redirect_page)
  except SelfassesmentTracker.DoesNotExist:
    messages.error(request, f'Selfassesment Tracker having id {tracker_id} does not exists!')
    return redirect(selfassesment_tracker_home_redirect_page)
    raise Http404

  if request.method == 'POST':
    form = SelfassesmentTrackerChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save(commit=False)
      if not assesment.issue_created_by and assesment.has_issue:
        assesment.issue_created_by = request.user
      if form.cleaned_data.get('is_completed')==True:
        assesment.complete_date = timezone.localtime()
        assesment.done_by = request.user
        assesment.has_issue = False
      assesment.save()
      messages.success(request, f'Selfassesment Tracker has been updated having id {tracker_id}!')
      if assesment.is_completed:
        return redirect(selfassesment_tracker_home_redirect_page)
    else:
      messages.error(request, f'Updating Selfassesment Tracker having id {tracker_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=selfassesment_tracker_home_redirect_page)
def delete_selfassesment_tracker(request, tracker_id:int):
  context = {
    **URLS,
    'page_title': 'Delete Selfassesment Tracker',
    'view_url': selfassesment_tracker_home_redirect_page,
    'id': tracker_id,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_delete_name,
    'form_title': "Selfassesment Tracker Delete Form",
    'form': SelfassesmentTrackerDeleteForm()
  }

  try:
    record =  SelfassesmentTracker.objects.get(tracker_id=tracker_id)
  except SelfassesmentTracker.DoesNotExist:
    messages.error(request, f'Selfassesment Tracker record with id {tracker_id}, you are looking for does not exist!')
    return redirect(selfassesment_tracker_home_redirect_page)

  if request.method == 'POST':
    form = SelfassesmentTrackerDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Selfassesment Tracker has been deleted having id {tracker_id}!')
    else:
      messages.error(request, f'Deletion of Selfassesment Tracker having id {tracker_id} failed')
    return redirect(selfassesment_tracker_home_redirect_page)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_selfassesment_tracker(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    # get search text from url query parameter
    search_text = request.GET.get('q', '').strip()
    client_id = request.GET.get('client_id', None)

    # if tasks query paramter exists then return tasks
    if request.GET.get('tasks'):
      tasks = {
        'new_customers': get_selfassesment_trackers_where_tasks_customers_are_new(),
        'future_incomplete_tasks': get_selfassesment_trackers_where_future_tasks_are_incomplete(),
        'todays_incomplete_tasks': get_selfassesment_trackers_where_todays_tasks_are_incomplete(),
        'previous_incomplete_tasks': get_selfassesment_trackers_where_previous_tasks_are_incomplete(),
        'task_has_issue': get_selfassesment_trackers_where_tasks_has_issues(),
        'my_tasks': get_selfassesment_trackers_where_tasks_assigned_to_user(request.user)
      }
      records = tasks.get(request.GET.get('tasks'), [])
      records.order_by('deadline')
      data = serialize(queryset=records, format='json')
      return HttpResponse(data, content_type='application/json')
    if not client_id==None:
      records = SelfassesmentTracker.objects.filter(client_id=client_id, is_completed=False)
      records.order_by('deadline')
      data = serialize(queryset=records, format='json')
      return HttpResponse(data, content_type='application/json')
    
    # filter results using the search_text
    if not search_text:
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_viewall_name)
    
    records = db_search_SelfassesmentTracker(
      search_text=search_text,
      user_email=request.user.email,
      is_superuser=request.user.is_superuser,
      limit=limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_selfassesment_tracker(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_SelfassesmentTracker(
      user_email=request.user.email,
      is_superuser=request.user.is_superuser,
      limit=limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def export_selfassesment_tracker(request):
  response = HttpResponse(
    content_type='text/csv; charset=utf-8',
    headers={'Content-Disposition': f'attachment; filename="selfassesment_tracker_{timezone.localtime()}.csv"'},
  )
  include_fields = []
  exclude_fields = set(['tracker_id', 'is_updated', 'creation_date'])
  fk_fields = {
    'client_id': SELFASSESMENT_FK_FIELDS_FOR_EXPORT
  }
  keep_include_fields = True
  show_others = True
  export_to_csv(
    django_model = SelfassesmentTracker,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others,
    fk_fields = fk_fields
    )
  return response


# =============================================================================================================
# =============================================================================================================
# Limited
@login_required
def home_limited(request):
  pk_field = 'client_id'
  exclude_fields = []
  include_fields = ['client_file_number', 'client_name', 'is_active', 'company_reg_number', 'company_auth_code', 'remarks', 'director_phone_number', 'director_email', 'UTR', 'NINO', 'HMRC_agent', "created_by", "date_of_registration"]
  keep_include_fields = True
  show_others = False
  model_fields = get_field_names_from_model(Limited)
  model_fields.append('incomplete_tasks')
  context = {
    **URLS,
    'caption': 'View Limited',
    'page_title': 'View Limited',

    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_create_name,
    'export_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_export_name,

    'template_tag': generate_template_tag_for_model(Limited, pk_field=pk_field, show_id=False, exclude_fields=exclude_fields, include_fields=include_fields, keep_include_fields=keep_include_fields, show_others=show_others),
    'data_container': generate_data_container_table(Limited, pk_field=pk_field, show_id=False, exclude_fields=exclude_fields, include_fields=include_fields, keep_include_fields=keep_include_fields, show_others=show_others),

    'frontend_data':{
      'all_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_viewall_url,
      'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_search_url,
      'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_update_url,
      'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_delete_url,  
      'model_fields': model_fields
    },
  }
  return render(request=request, template_name='companies/home.html', context=context)

@login_required
def view_limited(request):
  return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_home_name)

@login_required
def create_limited(request):
  context = {
    **URLS,
    'page_title': 'Create Limited',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_home_name,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_create_name,
    'form_title': 'Register Limited Company Form',
    'form': LimitedCreationForm(initial={'client_file_number': Limited.get_next_file_number()})
  }

  if request.method == 'POST':
    form = LimitedCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.set_defaults()
      assesment.created_by = request.user
      assesment.save()
      messages.success(request, f"New Limited has been created {assesment}!")

      # Create record in Limited Submission Deadline Tracker
      submission = LimitedSubmissionDeadlineTracker()
      submission.client_id = assesment
      submission.updated_by = request.user
      submission.save()
      messages.success(request, f'New Limited Submission has been created {submission}!')

      # Create record in Limited Confirmation Statement Tracker
      statement = LimitedConfirmationStatementTracker()
      statement.client_id = assesment
      statement.set_defaults(request)
      messages.success(request, f'New Limited Confirmation Statement has been created {submission}!')

      # Create record in Limited VAT Tracker
      if assesment.vat:
        for i in range(3):
          vat = LimitedVATTracker()
          vat.client_id = assesment
          vat.updated_by = request.user
          vat.save()
          messages.success(request, f'New Limited VAT Tracker has been created {vat}')
      context['form'] = LimitedCreationForm(initial={'client_file_number': Limited.get_next_file_number()})
  return render(request, template_name='companies/create.html', context=context)

@login_required
def get_details_limited(request, client_id=None):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    record = get_object_or_404(Limited, client_id=client_id)
    response = LimitedSerializer(instance=record).data
    return HttpResponse(json.dumps(response))
  raise Http404

@login_required
def update_limited(request, client_id:int):
  context = {
    **URLS,
    'page_title': f'Update Limited',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_home_name,
    'id': client_id,
    'update_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_update_name,
    'form_title': 'Limited Update Form',
    'form': LimitedChangeForm()
  }

  try:
    record = Limited.objects.get(client_id=client_id)
    had_vat = bool(record.vat)
    context['form'] = LimitedChangeForm(instance=record)
  except Limited.DoesNotExist:
    messages.error(request, f'Limited Account having id {client_id} does not exists!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_home_name)
    raise Http404

  if request.method == 'POST':
    form = LimitedChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      messages.success(request, f'Limited has been updated having id {client_id}!')
      
      if not had_vat and assesment.vat:
        # Create record in Limited VAT Tracker
        for i in range(3):
          vat = LimitedVATTracker()
          vat.client_id = record
          vat.updated_by = request.user
          vat.save()
          messages.success(request, f'New Limited VAT Tracker has been created {vat}')
    else:
      messages.error(request, f'Updating Limited {client_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_home_name)
def delete_limited(request, client_id:int):
  context = {
    **URLS,
    'page_title': 'Delte Limited',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_home_name,
    'id': client_id,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_delete_name,
    'form_title': "Limited Delete Form",
    'form': LimitedDeleteForm()
  }
  try:
    record =  Limited.objects.get(client_id=client_id)
  except Limited.DoesNotExist:
    messages.error(request, f'Limited record with id {client_id}, you are looking for does not exist!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_home_name)

  if request.method == 'POST':
    form = LimitedDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Limited has been deleted having id {client_id}!')
    else:
      messages.error(request, f'Limited deletion of id {client_id} failed!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_home_name)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_limited(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    search_text = request.GET.get('q', '')
    if search_text.strip()=='':
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Tracker_viewall_name)
    records = db_search_Limited(search_text, limit)
    records = records.order_by("-client_file_number")
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_limited(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_Limited(limit)
    records = records.order_by("-client_file_number")
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def export_limited(request):
  response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': f'attachment; filename="limited_{timezone.localtime()}.csv"'},
  )
  include_fields = ['is_active', 'client_file_number', 'client_name', 'company_reg_number', 'company_auth_code', 'remakrs', 'director_phone_number', 'director_email', 'UTR', 'NINO', 'HMRC_agent']
  exclude_fields = ['client_id',]
  keep_include_fields = True
  show_others = False
  export_to_csv(
    django_model = Limited,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others
    )
  return response



# =============================================================================================================
# =============================================================================================================
# LimitedTracker
limited_tracker_home_redirect_page = URL_NAMES_PREFIXED_WITH_APP_NAME.Merged_Tracker_home_name

def get_limited_trackers_where_tasks_customers_are_new():
  return LimitedTracker.objects.filter(new_customer=True, is_completed=False)

def get_limited_trackers_where_future_tasks_are_incomplete():
  return LimitedTracker.objects.filter(is_completed=False, deadline__gt=timezone.localtime())

def get_limited_trackers_where_todays_tasks_are_incomplete():
  return LimitedTracker.objects.filter(is_completed=False, deadline=timezone.localtime())

def get_limited_trackers_where_previous_tasks_are_incomplete():
  return LimitedTracker.objects.filter(deadline__lt=timezone.localtime(), is_completed=False)

def get_limited_trackers_where_tasks_has_issues():
  return LimitedTracker.objects.filter(has_issue=True)

def get_limited_trackers_where_tasks_assigned_to_user(user):
  return LimitedTracker.objects.filter(assigned_to=user, is_completed=False)

@login_required
def home_limited_tracker(request):
  pk_field = 'tracker_id'
  exclude_fields = set(['tracker_id', 'is_updated'])
  include_fields = ['tracker_id', 'client_id', 'job_description', 'deadline', 'remarks','is_completed', 'has_issue', 'complete_date', 'done_by', 'created_by','creation_date', 'issue_created_by']
  fk_fields = {
      'created_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'issue_created_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'done_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'submitted_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'prepared_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'assigned_to': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'client_id': { 'details_url_without_argument': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_details_url, 'repr-format': HTML_Generator.Limited_client_id_repr_format, 'href-url':Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_update_url },
      'incomplete_tasks': { 'details_url_without_argument': '/companies/SATrc/search/?client_id=', 'repr-format': r'{length}'}
      }

  keep_include_fields = True
  context = {
    **URLS,
    'page_title': 'View Limited Tracker',
    'caption': 'View Limited Tracker',
    
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Tracker_create_name,
    'export_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Tracker_export_name,
    
    'counts': True,
    'tracker_task_counts': True,
    'new_customers': get_limited_trackers_where_tasks_customers_are_new().count(),
    'future_incomplete_tasks': get_limited_trackers_where_future_tasks_are_incomplete().count(),
    'todays_incomplete_tasks': get_limited_trackers_where_todays_tasks_are_incomplete().count(),
    'previous_incomplete_tasks': get_limited_trackers_where_previous_tasks_are_incomplete().count(),
    'task_has_issue': get_limited_trackers_where_tasks_has_issues().count(),
    'my_tasks': get_limited_trackers_where_tasks_assigned_to_user(request.user).count(),

    'template_tag': generate_template_tag_for_model(LimitedTracker, pk_field=pk_field, show_id=True, include_fields=include_fields, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields, fk_fields=fk_fields),
    'data_container': generate_data_container_table(LimitedTracker, pk_field=pk_field, show_id=True, include_fields=include_fields, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),

    'frontend_data':{
      'all_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_viewall_url,
      'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_search_url,
      'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_update_url,
      'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_delete_url,  
      'model_fields': get_field_names_from_model(LimitedTracker)
    },
  }
  return render(request=request, template_name='companies/home.html', context=context)

@login_required
def view_limited_tracker(request):
  return redirect(limited_tracker_home_redirect_page)

@login_required
def create_limited_tracker(request):
  context = {
    **URLS,

    'page_title': 'Create Limited Tracker',
    'view_url': limited_tracker_home_redirect_page,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Tracker_create_name,
    'form_title': 'Limited Tracker Creation Form',
    'form': LimitedTrackerCreationForm(initial={'created_by': request.user.user_id})
  }
  redirect_to = None

  if request.method == 'POST':
    redirect_to = request.POST.get('redirect_to', None)
    form = LimitedTrackerCreationForm(request.POST, initial={'created_by': request.user.user_id})
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.created_by = request.user
      if not assesment.issue_created_by and assesment.has_issue:
        assesment.issue_created_by = request.user
      assesment.save()
      messages.success(request, f'New Limited Tracker has been created with id {assesment.tracker_id}!')
      context['form'] = LimitedTrackerCreationForm(initial={'created_by': request.user.user_id})

  try:
    if not redirect_to:
      redirect_to = request.GET.get('redirect_to', None)
    if redirect_to:
      return redirect(redirect_to)
  except NoReverseMatch:
    raise Http404
  return render(request, template_name='companies/create.html', context=context)

@login_required
def update_limited_tracker(request, tracker_id:int):
  context = {
    **URLS,
    'page_title': f'Update Limited Tracker',
    'view_url': limited_tracker_home_redirect_page,
    'id': tracker_id,
    'update_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Tracker_update_name,
    'form_title': 'Limited Update Form',
    'form': LimitedTrackerChangeForm()
  }

  try:
    record =  LimitedTracker.objects.get(tracker_id=tracker_id)
    context['form'] = LimitedTrackerChangeForm(instance=record)
    if record.is_completed:
      messages.error(request, message=f"Task {tracker_id} is completed therefore can't be updated!")
      return redirect(limited_tracker_home_redirect_page)
  except LimitedTracker.DoesNotExist:
    messages.error(request, f'Limited Tracker having id {tracker_id} does not exists!')
    return redirect(limited_tracker_home_redirect_page)
    raise Http404

  if request.method == 'POST':
    form = LimitedTrackerChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save(commit=False)
      if not assesment.issue_created_by and assesment.has_issue:
        assesment.issue_created_by = request.user
      if form.cleaned_data.get('is_completed')==True:
        assesment.complete_date = timezone.localtime()
        assesment.done_by = request.user
        assesment.has_issue = False
      assesment.save()
      messages.success(request, f'Limited Tracker has been updated having id {tracker_id}!')
      if assesment.is_completed:
        return redirect(limited_tracker_home_redirect_page)
    else:
      messages.error(request, f'Updating Limited Tracker having id {tracker_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Tracker_home_name)
def delete_limited_tracker(request, tracker_id:int):
  context = {
    **URLS,
    'page_title': 'Delete Limited Tracker',
    'view_url': limited_tracker_home_redirect_page,
    'id': tracker_id,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Tracker_delete_name,
    'form_title': "Limited Tracker Delete Form",
    'form': LimitedTrackerDeleteForm()
  }

  try:
    record =  LimitedTracker.objects.get(tracker_id=tracker_id)
  except LimitedTracker.DoesNotExist:
    messages.error(request, f'Limited Tracker record with id {tracker_id}, you are looking for does not exist!')
    return redirect(limited_tracker_home_redirect_page)

  if request.method == 'POST':
    form = LimitedTrackerDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Limited Tracker has been deleted having id {tracker_id}!')
    else:
      messages.error(request, f'Deletion of Limited Tracker having id {tracker_id} failed')
    return redirect(limited_tracker_home_redirect_page)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_limited_tracker(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    # get search text from url query parameter
    search_text = request.GET.get('q', '').strip()
    client_id = request.GET.get('client_id', None)

    # if tasks query paramter exists then return tasks
    if request.GET.get('tasks'):
      tasks = {
        'new_customers': LimitedTracker.objects.filter(new_customer=True),
        'future_incomplete_tasks': LimitedTracker.objects.filter(is_completed=False, deadline__gt=timezone.localtime()),
        'todays_incomplete_tasks': LimitedTracker.objects.filter(is_completed=False, deadline=timezone.localtime()),
        'previous_incomplete_tasks': LimitedTracker.objects.filter(deadline__lt=timezone.localtime(), is_completed=False),
        'task_has_issue': LimitedTracker.objects.filter(has_issue=True),
        'my_tasks': get_limited_trackers_where_tasks_assigned_to_user(request.user),
      }
      records = tasks.get(request.GET.get('tasks'), [])
      records.order_by('deadline')
      data = serialize(queryset=records, format='json')
      return HttpResponse(data, content_type='application/json')
    if not client_id==None:
      records = LimitedTracker.objects.filter(client_id=client_id, is_completed=False)
      records.order_by('deadline')
      data = serialize(queryset=records, format='json')
      return HttpResponse(data, content_type='application/json')
    
    # filter results using the search_text
    if not search_text:
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Tracker_viewall_name)
    
    records = db_search_LimitedTracker(
      search_text=search_text,
      user_email=request.user.email,
      is_superuser=request.user.is_superuser,
      limit=limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_limited_tracker(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_LimitedTracker(
      user_email=request.user.email,
      is_superuser=request.user.is_superuser,
      limit=limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def export_limited_tracker(request):
  response = HttpResponse(
    content_type='text/csv; charset=utf-8',
    headers={'Content-Disposition': f'attachment; filename="limited_tracker_{timezone.localtime()}.csv"'},
  )
  include_fields = []
  exclude_fields = set(['tracker_id', 'is_updated', 'creation_date'])
  fk_fields = {
    'client_id': LIMITED_FK_FIELDS_FOR_EXPORT
  }
  keep_include_fields = True
  show_others = True
  export_to_csv(
    django_model = LimitedTracker,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others,
    fk_fields = fk_fields
    )
  return response


# Limited Submission Deadline Tracker

# =============================================================================================================
# =============================================================================================================
# LimitedSubmissionDeadlineTracker
def get_limited_submissions_where_deadline_not_set():
  return LimitedSubmissionDeadlineTracker.objects.filter(HMRC_deadline = None)

def get_limited_submissions_where_deadline_missed():
  return LimitedSubmissionDeadlineTracker.objects.filter(HMRC_deadline__lt = timezone.now(), is_submitted=False)

def get_limited_submission_where_period_end(limit=-1):
    records = LimitedSubmissionDeadlineTracker.objects.filter(period__lt = timezone.now(), is_submitted=False).order_by()
    records = records.order_by('HMRC_deadline')
    if limit<=-1:
        return records
    return records[:limit]

@login_required
def home_limited_submission_deadline_tracker(request):
  pk_field = 'submission_id'
  exclude_fields = []
  field_ordering = ['client_id', 'period_start_date', 'period', 'remarks', 'HMRC_deadline', 'is_submitted', 'submitted_by', 'submission_date', 'our_deadline', 'is_submitted_hmrc', 'submitted_by_hmrc', 'submission_date_hmrc', 'is_documents_uploaded', ]
  keep_include_fields = False
  fk_fields = {
      'updated_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'submitted_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'submitted_by_hmrc': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'client_id': { 'details_url_without_argument': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_details_url, 'repr-format': HTML_Generator.Limited_client_id_repr_format, 'href-url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_update_url,},
      }
  context = {
    **URLS,
    'caption': 'View Limited Submission Deadline Tracker',
    'page_title': 'View Limited Submission Deadline Tracker',
    
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_create_name,
    'export_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_export_name,

    'counts': True,
    'limited_submission_counts': True,
    'submission_deadline_not_set': get_limited_submissions_where_deadline_not_set().count(),
    'submission_deadline_missed': get_limited_submissions_where_deadline_missed().count(),
    'submission_periodend': get_limited_submission_where_period_end().count(),

    'template_tag': generate_template_tag_for_model(LimitedSubmissionDeadlineTracker, show_id=False, pk_field=pk_field, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields, ordering=field_ordering, fk_fields=fk_fields),
    'data_container': generate_data_container_table(LimitedSubmissionDeadlineTracker, show_id=False, pk_field=pk_field, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields, ordering=field_ordering),

    'frontend_data':{
      'all_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Submission_Deadline_Tracker_viewall_url,
      'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Submission_Deadline_Tracker_search_url,
      'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Submission_Deadline_Tracker_update_url,
      'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Submission_Deadline_Tracker_delete_url,  
      'model_fields': get_field_names_from_model(LimitedSubmissionDeadlineTracker)
    },
  }
  return render(request=request, template_name='companies/home.html', context=context)

@login_required
def view_limited_submission_deadline_tracker(request):
  return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name)

@login_required
def create_limited_submission_deadline_tracker(request):
  context = {
    **URLS,

    'page_title': 'Create Limited Submission Deadline Tracker',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_create_name,
    'form_title': 'Limited Submission Deadline Tracker Creation Form',
    'form': LimitedSubmissionDeadlineTrackerCreationForm()
  }

  if request.method == 'POST':
    form = LimitedSubmissionDeadlineTrackerCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.set_defaults(request)
      assesment.save()
      messages.success(request, f'New Limited Submission Deadline Tracker has been created with id {assesment.submission_id}!')
      context['form'] = LimitedSubmissionDeadlineTrackerCreationForm()
    else:
      messages.error(request, f'Action failed due to invalid data!')
  return render(request, template_name='companies/create.html', context=context)

@login_required
def update_limited_submission_deadline_tracker(request, submission_id:int):
  context = {
    **URLS,
    'page_title': f'Update Limited Submission Deadline Tracker',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name,
    'id': submission_id,
    'update_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_update_name,
    'form_title': 'Limited Submission Deadline Tracker Update Form',
    'form': LimitedSubmissionDeadlineTrackerChangeForm()
  }

  try:
    record =  LimitedSubmissionDeadlineTracker.objects.get(submission_id=submission_id)
    if record.is_submitted and record.is_submitted_hmrc:
      messages.error(request, message=f"Limited Submission Deadline Tracker {submission_id} is submitted therefore can't be updated!")
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name)
    context['form'] = LimitedSubmissionDeadlineTrackerChangeForm(instance=record)
  except LimitedSubmissionDeadlineTracker.DoesNotExist:
    messages.error(request, f'Limited Submission Deadline Tracker having id {submission_id} does not exist!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name)
    raise Http404

  if request.method == 'POST':
    form = LimitedSubmissionDeadlineTrackerChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save(commit=False)
      assesment.set_defaults(request)
      assesment.save()
      context['form'] = LimitedSubmissionDeadlineTrackerChangeForm(instance=assesment)
      messages.success(request, f'Limited Submission Deadline Tracker has been updated having id {submission_id}!')

      if assesment.is_submitted and not assesment.submitted_by:
        assesment.submitted_by = request.user
        assesment.save()
      else:
        assesment.submitted_by = None
        assesment.save()

      if assesment.is_submitted_hmrc and not assesment.submitted_by_hmrc:
        assesment.submitted_by_hmrc = request.user
        assesment.save()
      else:
        assesment.submitted_by_hmrc = None
        assesment.save()

      if assesment.is_submitted and assesment.is_submitted_hmrc:
        new_assesment = LimitedSubmissionDeadlineTracker()
        new_assesment.client_id = assesment.client_id
        new_assesment.updated_by = request.user
        new_assesment.HMRC_deadline = assesment.HMRC_deadline + relativedelta(years=1) # Compnay House deadline
        new_assesment.our_deadline = assesment.our_deadline + relativedelta(years=1) # HMRC Deadline
        new_assesment.save()
        messages.success(request, f'New Limited Submission Deadline Tracker has been created {new_assesment}')
        return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name)
    else:
      messages.error(request, f'Updating Limited Submission Deadline Tracker having id {submission_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name)
def delete_limited_submission_deadline_tracker(request, submission_id:int):
  context = {
    **URLS,
    'page_title': 'Delete Limited Submission Deadline Tracker',
    'id': submission_id,
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_delete_name,
    'form_title': "Limited Submission Deadline Tracker Delete Form",
    'form': LimitedSubmissionDeadlineTrackerDeleteForm()
  }

  try:
    record = LimitedSubmissionDeadlineTracker.objects.get(submission_id=submission_id)
  except LimitedSubmissionDeadlineTracker.DoesNotExist:
    messages.error(request, f'Limited Submission Deadline Tracker record with id {submission_id}, you are looking for does not exist!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name)
  
  if request.method == 'POST':
    form = LimitedSubmissionDeadlineTrackerDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Limited Submission Deadline Tracker has been deleted having id {submission_id}!')
    else:
      messages.error(request, f'Deletion of Limited Submission Deadline Tracker having id {submission_id} failed!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_home_name)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_limited_submission_deadline_tracker(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    # get search text from url query parameter
    search_text = request.GET.get('q', '').strip()
    tasks_key = request.GET.get('tasks')

    # if tasks query paramter exists then return tasks
    if tasks_key:
      tasks = {
        'submission_deadline_not_set': get_limited_submissions_where_deadline_not_set(),
        'submission_deadline_missed': get_limited_submissions_where_deadline_missed(),
        'submission_periodend': get_limited_submission_where_period_end(),
      }
      records = tasks.get(tasks_key, [])
      data = serialize(queryset=records, format='json')
      return HttpResponse(data, content_type='application/json')
    
    # filter results using the search_text
    if search_text.strip()=='':
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Submission_Deadline_Tracker_viewall_name)
    records = db_search_LimitedSubmissionDeadlineTracker(search_text, limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_limited_submission_deadline_tracker(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_LimitedSubmissionDeadlineTracker(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def export_limited_submission_deadline_tracker(request):
  response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': f'attachment; filename="limited_submission_deadline_tracker_{timezone.localtime()}.csv"'},
  )
  include_fields = []
  exclude_fields = ['submission_id']
  fk_fields = {
    'client_id': LIMITED_FK_FIELDS_FOR_EXPORT
  }
  keep_include_fields = False
  show_others = True
  export_to_csv(
    django_model = LimitedSubmissionDeadlineTracker,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others,
    fk_fields = fk_fields
    )
  return response


# =============================================================================================================
# =============================================================================================================
# LimitedVATTracker
def get_limited_vats_where_deadline_not_set():
  return LimitedVATTracker.objects.filter(HMRC_deadline = None)

def get_limited_vats_where_deadline_missed():
  return LimitedVATTracker.objects.filter(HMRC_deadline__lt = timezone.now(), is_submitted=False)

def get_limited_vats_where_period_difference_more_than_3months():
  return LimitedVATTracker.objects.annotate(
  diff=ExpressionWrapper(F('period_end') - F('period_start') , 
  output_field=DurationField())).filter(diff__gte=timedelta(90), is_submitted=False)

@login_required
def home_limited_vat_tracker(request):
  pk_field = 'vat_id'
  exclude_fields = []
  field_ordering = ['client_id', 'period_start', 'period_end', 'HMRC_deadline', 'remarks',]
  keep_include_fields = True
  fk_fields = {
      'updated_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'submitted_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'client_id': { 'details_url_without_argument': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_details_url, 'repr-format': HTML_Generator.Limited_client_id_repr_format, 'href-url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_update_url,},
      }
  context = {
    **URLS,
    'caption': 'View VAT Tracker',
    'page_title': 'View VAT Tracker',
    
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_create_name,
    'export_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_export_name,

    'counts': True,
    'limited_vat_counts': True,
    'submission_deadline_not_set': get_limited_vats_where_deadline_not_set().count(),
    'submission_deadline_missed': get_limited_vats_where_deadline_missed().count(),
    'period_diff_gt_3months': get_limited_vats_where_period_difference_more_than_3months().count(),

    'template_tag': generate_template_tag_for_model(LimitedVATTracker, pk_field=pk_field, show_id=False, ordering=field_ordering, fk_fields=fk_fields),
    'data_container': generate_data_container_table(LimitedVATTracker, pk_field=pk_field, show_id=False, ordering=field_ordering),

    'frontend_data':{
      'all_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_VAT_Tracker_viewall_url,
      'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_VAT_Tracker_search_url,
      'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_VAT_Tracker_update_url,
      'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_VAT_Tracker_delete_url,  
      'model_fields': get_field_names_from_model(LimitedVATTracker)
    },
  }
  return render(request=request, template_name='companies/home.html', context=context)

@login_required
def view_limited_vat_tracker(request):
  return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name)

@login_required
def create_limited_vat_tracker(request):
  context = {
    **URLS,

    'page_title': 'Create Limited VAT Tracker',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_create_name,
    'form_title': 'Limited VAT Tracker Creation Form',
    'form': LimitedVATTrackerCreationForm()
  }

  if request.method == 'POST':
    form = LimitedVATTrackerCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.set_defaults(request)
      assesment.save()
      messages.success(request, f'New Limited VAT Tracker has been created with id {assesment.vat_id}!')
      context['form'] = LimitedVATTrackerCreationForm()
    else:
      messages.error(request, f'Action failed due to invalid data!')
  return render(request, template_name='companies/create.html', context=context)

@login_required
def update_limited_vat_tracker(request, vat_id:int):
  context = {
    **URLS,
    'page_title': f'Update Limited VAT Tracker',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name,
    'id': vat_id,
    'update_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_update_name,
    'form_title': 'Limited VAT Tracker Update Form',
    'form': LimitedVATTrackerChangeForm()
  }

  try:
    record =  LimitedVATTracker.objects.get(vat_id=vat_id)
    if record.is_submitted:
      messages.error(request, message=f"Limited VAT Tracker {vat_id} is submitted therefore can't be updated!")
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name)
    context['form'] = LimitedVATTrackerChangeForm(instance=record)
  except LimitedVATTracker.DoesNotExist:
    messages.error(request, f'Limited VAT Tracker having id {vat_id} does not exists!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name)
    raise Http404

  if request.method == 'POST':
    form = LimitedVATTrackerChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save(commit=False)
      assesment.set_defaults(request)
      assesment.save()
      
      # Create Limited VAT Tracker
      if assesment.is_submitted:
        vat = LimitedVATTracker()
        vat.client_id = assesment.client_id
        vat.updated_by = request.user
        vat.save()
        messages.success(request, f'New Limited VAT Tracker has been created {vat}')

      context['form'] = LimitedVATTrackerChangeForm(instance=assesment)
      messages.success(request, f'Limited VAT Tracker has been updated having id {vat_id}!')
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name)
    else:
      messages.error(request, f'Updating Limited VAT Tracker having id {vat_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name)
def delete_limited_vat_tracker(request, vat_id:int):
  context = {
    **URLS,
    'page_title': 'Delete Limited VAT Tracker',
    'id': vat_id,
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_delete_name,
    'form_title': "Limited VAT Tracker Delete Form",
    'form': LimitedVATTrackerDeleteForm()
  }

  try:
    record = LimitedVATTracker.objects.get(vat_id=vat_id)
  except LimitedVATTracker.DoesNotExist:
    messages.error(request, f'Limited VAT Tracker record with id {vat_id}, you are looking for does not exist!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name)
  
  if request.method == 'POST':
    form = LimitedVATTrackerDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Limited VAT Tracker has been deleted having id {vat_id}!')
    else:
      messages.error(request, f'Deletion of Limited VAT Tracker having id {vat_id} failed!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_home_name)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_limited_vat_tracker(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    # get search text from url query parameter
    search_text = request.GET.get('q', '').strip()
    tasks_key = request.GET.get('tasks')

    # if tasks query paramter exists then return tasks
    if tasks_key:
      tasks = {
        'submission_deadline_not_set': get_limited_vats_where_deadline_not_set(),
        'submission_deadline_missed': get_limited_vats_where_deadline_missed(),
        'period_diff_gt_3months': get_limited_vats_where_period_difference_more_than_3months()
      }
      records = tasks.get(tasks_key, [])
      data = serialize(queryset=records, format='json')
      return HttpResponse(data, content_type='application/json')
    
    # filter results using the search_text
    if search_text.strip()=='':
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_VAT_Tracker_viewall_name)
    records = db_search_LimitedVATTracker(search_text, limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_limited_vat_tracker(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_LimitedVATTracker(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def export_limited_vat_tracker(request):
  response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': f'attachment; filename="limited_vat_tracker_{timezone.localtime()}.csv"'},
  )
  include_fields = []
  fk_fields = {
    'client_id': LIMITED_FK_FIELDS_FOR_EXPORT
  }
  exclude_fields = ['vat_id']
  keep_include_fields = False
  show_others = True
  export_to_csv(
    django_model = LimitedVATTracker,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others,
    fk_fields = fk_fields
    )
  return response


# =============================================================================================================
# =============================================================================================================
# LimitedConfirmationStatementTracker
def get_limited_statements_where_deadline_not_set():
  return LimitedConfirmationStatementTracker.objects.filter(HMRC_deadline = None)

def get_limited_statements_where_deadline_missed():
  return LimitedConfirmationStatementTracker.objects.filter(HMRC_deadline__lt = timezone.now(), is_submitted=False)


@login_required
def home_limited_confirmation_statement_tracker(request):
  pk_field = 'statement_id'
  keep_include_fields = True
  fk_fields = {
      'updated_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'submitted_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
      'client_id': { 'details_url_without_argument': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_details_url, 'repr-format': HTML_Generator.Limited_client_id_repr_format, 'href-url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_update_url,},
      }
  context = {
    **URLS,
    'caption': 'View Confirmation Statement Tracker',
    'page_title': 'View Confirmation Statement Tracker',
    
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_create_name,
    'export_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_export_name,

    'counts': True,
    'limited_statement_counts': True,
    'statement_deadline_not_set': get_limited_statements_where_deadline_not_set().count(),
    'statement_deadline_missed': get_limited_statements_where_deadline_missed().count(),

    'template_tag': generate_template_tag_for_model(LimitedConfirmationStatementTracker, pk_field=pk_field, show_id=True, fk_fields=fk_fields),
    'data_container': generate_data_container_table(LimitedConfirmationStatementTracker, pk_field=pk_field, show_id=True),

    'frontend_data':{
      'all_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Confirmation_Statement_Tracker_viewall_url,
      'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Confirmation_Statement_Tracker_search_url,
      'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Confirmation_Statement_Tracker_update_url,
      'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Confirmation_Statement_Tracker_delete_url,  
      'model_fields': get_field_names_from_model(LimitedConfirmationStatementTracker)
    },
  }
  return render(request=request, template_name='companies/home.html', context=context)

@login_required
def view_limited_confirmation_statement_tracker(request):
  return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name)

@login_required
def create_limited_confirmation_statement_tracker(request):
  context = {
    **URLS,

    'page_title': 'Create Limited Confirmation Statement Tracker',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_create_name,
    'form_title': 'Limited Confirmation Statement Tracker Creation Form',
    'form': LimitedConfirmationStatementTrackerCreationForm()
  }

  if request.method == 'POST':
    form = LimitedConfirmationStatementTrackerCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.set_defaults(request)
      assesment.save()
      messages.success(request, f'New Limited Confirmation Statement Tracker has been created with id {assesment.statement_id}!')
      context['form'] = LimitedConfirmationStatementTrackerCreationForm()
    else:
      messages.error(request, f'Action failed due to invalid data!')
  return render(request, template_name='companies/create.html', context=context)

@login_required
def update_limited_confirmation_statement_tracker(request, statement_id:int):
  context = {
    **URLS,
    'page_title': f'Update Limited Confirmation Statement Tracker',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name,
    'id': statement_id,
    'update_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_update_name,
    'form_title': 'Limited Confirmation Statement Tracker Update Form',
    'form': LimitedConfirmationStatementTrackerChangeForm()
  }

  try:
    record =  LimitedConfirmationStatementTracker.objects.get(statement_id=statement_id)
    if record.is_submitted:
      messages.error(request, message=f"Limited Confirmation Statement Tracker {statement_id} is submitted therefore can't be updated!")
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name)
    context['form'] = LimitedConfirmationStatementTrackerChangeForm(instance=record)
  except LimitedConfirmationStatementTracker.DoesNotExist:
    messages.error(request, f'Limited Confirmation Statement Tracker having id {statement_id} does not exists!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name)
    raise Http404

  if request.method == 'POST':
    form = LimitedConfirmationStatementTrackerChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save(commit=False)
      assesment.set_defaults(request)
      assesment.save()
      
      # Create Limited Confirmation Statement Tracker
      if assesment.is_submitted:
        statement = LimitedConfirmationStatementTracker()
        statement.client_id = assesment.client_id
        statement.set_defaults(request)
        statement.save()
        messages.success(request, f'New Limited Confirmation Statement Tracker has been created {statement}!')

      context['form'] = LimitedConfirmationStatementTrackerChangeForm(instance=assesment)
      messages.success(request, f'Limited Confirmation Statement Tracker has been updated having id {statement_id}!')
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name)
    else:
      messages.error(request, f'Updating Limited Confirmation Statement Tracker having id {statement_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name)
def delete_limited_confirmation_statement_tracker(request, statement_id:int):
  context = {
    **URLS,
    'page_title': 'Delete Limited Confirmation Statement Tracker',
    'id': statement_id,
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_delete_name,
    'form_title': "Limited Confirmation Statement Tracker Delete Form",
    'form': LimitedConfirmationStatementTrackerDeleteForm()
  }

  try:
    record = LimitedConfirmationStatementTracker.objects.get(statement_id=statement_id)
  except LimitedConfirmationStatementTracker.DoesNotExist:
    messages.error(request, f'Limited Confirmation Statement Tracker record with id {statement_id}, you are looking for does not exist!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name)
  
  if request.method == 'POST':
    form = LimitedConfirmationStatementTrackerDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Limited Confirmation Statement Tracker has been deleted having id {statement_id}!')
    else:
      messages.error(request, f'Deletion of Limited Confirmation Statement Tracker having id {statement_id} failed!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_home_name)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_limited_confirmation_statement_tracker(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    # get search text from url query parameter
    search_text = request.GET.get('q', '').strip()
    tasks_key = request.GET.get('tasks')

    # if tasks query paramter exists then return tasks
    if tasks_key:
      tasks = {
        'statement_deadline_not_set': get_limited_statements_where_deadline_not_set(),
        'statement_deadline_missed': get_limited_statements_where_deadline_missed(),
      }
      records = tasks.get(tasks_key, [])
      data = serialize(queryset=records, format='json')
      return HttpResponse(data, content_type='application/json')
    
    # filter results using the search_text
    if search_text.strip()=='':
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Confirmation_Statement_Tracker_viewall_name)
    records = db_search_LimitedConfirmationStatementTracker(search_text, limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_limited_confirmation_statement_tracker(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_LimitedConfirmationStatementTracker(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def export_limited_confirmation_statement_tracker(request):
  response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': f'attachment; filename="limited_confirmation_statement_tracker_{timezone.localtime()}.csv"'},
  )
  include_fields = []
  exclude_fields = ['statement_id']
  fk_fields = {
    'client_id': LIMITED_FK_FIELDS_FOR_EXPORT
  }
  keep_include_fields = False
  show_others = True
  export_to_csv(
    django_model = LimitedConfirmationStatementTracker,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others,
    fk_fields = fk_fields
    )
  return response


###########################################
# Merged trackers view
merged_tracker_home_redirect_page = URL_NAMES_PREFIXED_WITH_APP_NAME.Merged_Tracker_home_name

@login_required
def home_merged_tracker(request):
  pk_field = 'tracker_id'
  exclude_fields = ['is_updated']
  include_fields = ['tracker_id', 'client_id', 'job_description', 'deadline', 'remarks','is_completed', 'has_issue', 'complete_date', 'done_by', 'created_by','creation_date', 'issue_created_by']
  limited_tracker_fk_fields = {
    'created_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'issue_created_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'done_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'submitted_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'prepared_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'assigned_to': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'client_id': { 'details_url_without_argument': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_details_url, 'repr-format': HTML_Generator.Limited_client_id_repr_format, 'href-url':Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_update_url },
    'incomplete_tasks': { 'details_url_without_argument': '/companies/LTrc/search/?client_id=', 'repr-format': r'{length}'}
    }
  selfassesment_tracker_fk_fields = {
    'created_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'issue_created_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'done_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'submitted_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'prepared_by': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'assigned_to': { 'details_url_without_argument': user_details_url_without_argument, 'repr-format': HTML_Generator.CustomUser_repr_format },
    'client_id': { 'details_url_without_argument': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_details_url, 'repr-format': HTML_Generator.Selfassesment_client_id_repr_format, 'href-url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_update_url },
    'incomplete_tasks': { 'details_url_without_argument': '/companies/SATrc/search/?client_id=', 'repr-format': r'{length}'}
    }

  keep_include_fields = True
  context = {
    **URLS,
    'page_title': 'View Tracker',
    'caption': 'View Tracker',

    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Merged_Tracker_create_name,
    'export_name': URL_NAMES_PREFIXED_WITH_APP_NAME.Merged_Tracker_export_name,

    'create_limited_tracker': URL_NAMES_PREFIXED_WITH_APP_NAME.Limited_Tracker_create_name,
    'create_selfassesment_tracker': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_create_name,

    'counts': True,
    'tracker_task_counts': True,
    'new_customers': get_limited_trackers_where_tasks_customers_are_new().count() + get_selfassesment_trackers_where_tasks_customers_are_new().count(),
    'future_incomplete_tasks': get_limited_trackers_where_future_tasks_are_incomplete().count() + get_selfassesment_trackers_where_future_tasks_are_incomplete().count(),
    'todays_incomplete_tasks': get_limited_trackers_where_todays_tasks_are_incomplete().count() + get_selfassesment_trackers_where_todays_tasks_are_incomplete().count(),
    'previous_incomplete_tasks': get_limited_trackers_where_previous_tasks_are_incomplete().count() + get_selfassesment_trackers_where_previous_tasks_are_incomplete().count(),
    'task_has_issue': get_limited_trackers_where_tasks_has_issues().count() + get_selfassesment_trackers_where_tasks_has_issues().count(),
    'my_tasks': get_limited_trackers_where_tasks_assigned_to_user(request.user).count() + get_selfassesment_trackers_where_tasks_assigned_to_user(request.user).count(),

    'data_container': generate_data_container_table(LimitedTracker, pk_field=pk_field, show_id=True, include_fields=include_fields, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),
    'selfassesment_tracker_template': generate_template_tag_for_model(SelfassesmentTracker, pk_field=pk_field, show_id=True, include_fields=include_fields, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields, fk_fields=selfassesment_tracker_fk_fields, tag_id="selfassesment_tracker_template"),
    'limited_tracker_template': generate_template_tag_for_model(LimitedTracker, pk_field=pk_field, show_id=True, include_fields=include_fields, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields, fk_fields=limited_tracker_fk_fields, tag_id="limited_tracker_template"),

    'frontend_data': {
      "Limited": {
        'create_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_create_url,
        'viewall_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_viewall_url,
        'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_search_url,
        'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_update_url,
        'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_delete_url,
        "model_fields": get_field_names_from_model(SelfassesmentTracker),
      },
      "Selfassesment": {
        'create_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_create_url,
        'viewall_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_viewall_url,
        'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_search_url,
        'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_update_url,
        'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_delete_url,
        "model_fields": get_field_names_from_model(LimitedTracker),
      },
    },
  }
  return render(request, 'companies/merged_tracker.html', context=context)

@login_required
def create_merged_tracker(request):
  context = {
    **URLS,
    'page_title': 'Create Tracker',
    
    'view_url': merged_tracker_home_redirect_page,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Merged_Tracker_create_name,

    'form_title': 'Tracker Creation Form',
    'form': MergedTrackerCreateionForm(),

    'redirect_to': URL_NAMES_PREFIXED_WITH_APP_NAME.Merged_Tracker_create_name,

    'frontend_data':{
      "Limited": {
        'create_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_Tracker_create_url,
        'viewall_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_viewall_url,
        'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Limited_search_url,
        'repr_format': FK_Formats.Limited_client_id_repr_format,
        'redirect_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Merged_Tracker_create_name
      },
      "Selfassesment": {
        'create_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_create_url,
        'viewall_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_viewall_url,
        'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_search_url,
        'repr_format': FK_Formats.Selfassesment_client_id_repr_format,
        'redirect_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Merged_Tracker_create_name
      },
    }
  }
  return render(request, template_name='companies/merged_tracker_create.html', context=context)

@login_required
def export_merged_tracker(request):
  response = HttpResponse(
    content_type='text/csv; charset=utf-8',
    headers={'Content-Disposition': f'attachment; filename="merged_tracker_{timezone.localtime()}.csv"'},
  )
  include_fields = []
  exclude_fields = set(['is_updated'])
  keep_include_fields = True
  show_others = True
  export_to_csv(
    django_model = LimitedTracker,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others
    )
  export_to_csv(
    django_model = SelfassesmentTracker,
    write_to = response,
    include_fields = include_fields,
    exclude_fields = exclude_fields,
    keep_include_fields = keep_include_fields,
    show_others = show_others,
    write_header_row=False
    )
  return response
