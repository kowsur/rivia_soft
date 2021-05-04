import json
from django.http.response import Http404, HttpResponse
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

#forms
from .forms import SelfassesmentCreationForm, SelfassesmentChangeForm, SelfassesmentDeleteForm
from .forms import SelfassesmentAccountSubmissionCreationForm, SelfassesmentAccountSubmissionChangeForm, SelfassesmentAccountSubmissionDeleteForm
from .forms import Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form
from .forms import SelfassesmentTrackerCreationForm, SelfassesmentTrackerChangeForm, SelfassesmentTrackerDeleteForm

#models
from .models import Selfassesment, SelfassesmentAccountSubmission
from .models import SelfassesmentTracker

#queries
from .queries import db_search_Selfassesment, db_all_Selfassesment
from .queries import db_search_SelfassesmentAccountSubmission, db_all_SelfassesmentAccountSubmission
from .queries import db_search_SelfassesmentTracker, db_all_SelfassesmentTracker

# serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer, SelfassesmentSerializer

#permissions
from .decorators import allowed_for_staff, allowed_for_superuser


from .url_variables import APPLICATION_NAME, URL_NAMES, URL_PATHS, Full_URL_PATHS_WITHOUT_ARGUMENTS, URL_NAMES_PREFIXED_WITH_APP_NAME
from .url_variables import *

# html generator
from .html_generator import get_field_names_from_model, generate_template_tag_for_model, generate_data_container_table

application_name = APPLICATION_NAME
# these path names will be passed to templates to use in the navbar links
URLS = {
  'home': f'{application_name}:home',

  **Full_URL_PATHS_WITHOUT_ARGUMENTS.get_dict(),
  **URL_NAMES_PREFIXED_WITH_APP_NAME.get_dict()
}

# =============================================================================================================
# =============================================================================================================
# Selfassesment
@login_required
def home_selfassesment(request):
  pk_field = 'client_id'
  exclude_fields = []
  include_fields = ['is_active', 'client_file_number', 'client_name', 'personal_phone_number', 'personal_email', 'UTR', 'NINO', 'HMRC_agent']
  keep_include_fields = True
  show_others = False
  context = {
    **URLS,
    'model_fields': get_field_names_from_model(Selfassesment),
    'template_tag': generate_template_tag_for_model(Selfassesment, pk_field=pk_field, exclude_fields=exclude_fields, include_fields=include_fields, keep_include_fields=keep_include_fields, show_others=show_others),
    'data_container': generate_data_container_table(Selfassesment, pk_field=pk_field, exclude_fields=exclude_fields, include_fields=include_fields, keep_include_fields=keep_include_fields, show_others=show_others),

    'caption': 'View Selfassesment',
    'page_title': 'View Selfassesment',
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_create_name,
    'viewall_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_viewall_url,
    'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_search_url,
    'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_update_url,
    'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_delete_url,
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
      messages.success(request, f'New Selfassesment has been created with id {assesment.client_id}!')
      context['form'] = SelfassesmentCreationForm(initial={'client_file_number': Selfassesment.get_next_file_number()})
  return render(request, template_name='companies/create.html', context=context)

@login_required
def get_details_selfassesment(request, client_id=None):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    record = get_object_or_404(Selfassesment, client_id=client_id)
    response = SelfassesmentSerializer(instance=record).data
    return HttpResponse(json.dumps(response))
  raise Http404

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
    'page_title': '',
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
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_selfassesment(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_Selfassesment(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@api_view(['GET'])
def serialized(request):
  
  return SelfassesmentSerializer()

# =============================================================================================================
# =============================================================================================================
# SelfassesmentAccountSubmission
@login_required
def home_selfassesment_account_submission(request):
  pk_field = 'submission_id'
  exclude_fields = []
  keep_include_fields = True
  context = {
    **URLS,
    'model_fields': get_field_names_from_model(SelfassesmentAccountSubmission),
    'template_tag': generate_template_tag_for_model(SelfassesmentAccountSubmission, pk_field=pk_field, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),
    'data_container': generate_data_container_table(SelfassesmentAccountSubmission, pk_field=pk_field, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),
    
    'caption': 'View Selfassesment Account Submission',
    'page_title': 'View Selfassesment Account Submission',
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_create_name,
    'viewall_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Account_Submission_viewall_url,
    'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Account_Submission_search_url,
    'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Account_Submission_update_url,
    'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Account_Submission_delete_url,
    'add_all_url': URL_NAMES_PREFIXED_WITH_APP_NAME.add_all_Selfassesment_to_Selfassesment_Account_Submission_name,
    'add_all_text': 'Add all Selfassesment to Selfassesment Account Submission'
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
    'form': SelfassesmentAccountSubmissionCreationForm(initial={'submitted_by': request.user.user_id})
  }

  if request.method == 'POST':
    form = SelfassesmentAccountSubmissionCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      if not assesment.submitted_by:
        assesment.submitted_by = request.user
      assesment.set_defaults()
      messages.success(request, f'New Selfassesment Account Submission has been created with id {assesment.submission_id}!')
      context['form'] = SelfassesmentAccountSubmissionCreationForm(initial={'submitted_by': request.user.user_id})
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
      assesment = form.save()
      messages.success(request, f'Selfassesment Account Submission has been updated having id {submission_id}!')
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
        instance.save()
      messages.success(request, 'Added all Selfassesment to Selfassesment Account Submission!')
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Account_Submission_home_name)
  return render(request, 'companies/create.html', context=context)


# =============================================================================================================
# =============================================================================================================
# SelfassesmentTracker
@login_required
def home_selfassesment_tracker(request):
  pk_field = 'tracker_id'
  exclude_fields = set(['tracker_id', 'is_updated', 'creation_date'])
  keep_include_fields = False
  context = {
    **URLS,
    'model_fields': get_field_names_from_model(SelfassesmentTracker),
    'template_tag': generate_template_tag_for_model(SelfassesmentTracker, pk_field=pk_field, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),
    'data_container': generate_data_container_table(SelfassesmentTracker, pk_field=pk_field, exclude_fields=exclude_fields, keep_include_fields=keep_include_fields),
    
    'page_title': 'View Selfassesment Tracker',
    'caption': 'View Selfassesment Tracker',
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_create_name,
    'viewall_url': Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_viewall_url,
    'search_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_search_url,
    'update_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_update_url,
    'delete_url':  Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_Tracker_delete_url,
    'task_counts': True,
    'completed_tasks': SelfassesmentTracker.objects.filter(is_completed=True).count(),
    'future_taks': SelfassesmentTracker.objects.filter(is_completed=False, deadline__gt=timezone.now()).count(),
    'todays_taks': SelfassesmentTracker.objects.filter(is_completed=False, deadline=timezone.now()).count(),
    'previous_tasks': SelfassesmentTracker.objects.filter(deadline__lt=timezone.now(), is_completed=False).count(),
  }
  return render(request=request, template_name='companies/home.html', context=context)

@login_required
def view_selfassesment_tracker(request):
  return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_home_name)

@login_required
def create_selfassesment_tracker(request):
  context = {
    **URLS,

    'page_title': 'Create Selfassesment Tracker',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_home_name,
    'create_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_create_name,
    'form_title': 'Selfassesment Tracker Creation Form',
    'form': SelfassesmentTrackerCreationForm(initial={'created_by': request.user.user_id})
  }

  if request.method == 'POST':
    form = SelfassesmentTrackerCreationForm(request.POST, initial={'created_by': request.user.user_id})
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.created_by = request.user
      assesment.save()
      messages.success(request, f'New Selfassesment Tracker has been created with id {assesment.tracker_id}!')
      context['form'] = SelfassesmentTrackerCreationForm(initial={'created_by': request.user.user_id})
  return render(request, template_name='companies/create.html', context=context)

@login_required
def update_selfassesment_tracker(request, tracker_id:int):
  context = {
    **URLS,
    'page_title': f'Update Selfassesment Tracker',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_home_name,
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
      return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_home_name)
  except SelfassesmentTracker.DoesNotExist:
    messages.error(request, f'Selfassesment Tracker having id {tracker_id} does not exists!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_home_name)
    raise Http404

  if request.method == 'POST':
    form = SelfassesmentTrackerChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save(commit=False)
      assesment.done_by = request.user
      if form.cleaned_data.get('is_completed')==True:
        assesment.complete_date = timezone.now()
      assesment.save()
      messages.success(request, f'Selfassesment Tracker has been updated having id {tracker_id}!')
    else:
      messages.error(request, f'Updating Selfassesment Tracker having id {tracker_id} failed due to invalid data!')
  return render(request, template_name='companies/update.html', context=context)

@login_required
@allowed_for_superuser(
  message="Sorry! You are not authorized to delete this.",
  redirect_to=URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_home_name)
def delete_selfassesment_tracker(request, tracker_id:int):
  context = {
    **URLS,
    'page_title': 'Delete Selfassesment Tracker',
    'view_url': URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_home_name,
    'id': tracker_id,
    'delete_url':  URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_delete_name,
    'form_title': "Selfassesment Tracker Delete Form",
    'form': SelfassesmentTrackerDeleteForm()
  }

  try:
    record =  SelfassesmentTracker.objects.get(tracker_id=tracker_id)
  except SelfassesmentTracker.DoesNotExist:
    messages.error(request, f'Selfassesment Tracker record with id {tracker_id}, you are looking for does not exist!')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_home_name)

  if request.method == 'POST':
    form = SelfassesmentTrackerDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      record.delete()
      messages.success(request, f'Selfassesment Tracker has been deleted having id {tracker_id}!')
    else:
      messages.error(request, f'Deletion of Selfassesment Tracker having id {tracker_id} failed')
    return redirect(URL_NAMES_PREFIXED_WITH_APP_NAME.Selfassesment_Tracker_home_name)
  return render(request, template_name='companies/delete.html', context=context)

@login_required
def search_selfassesment_tracker(request, limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    search_text = request.GET.get('q', '')
    if search_text.strip()=='':
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
