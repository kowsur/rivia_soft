from django.http.response import Http404, HttpResponse
from django.core.serializers import serialize
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

#forms
from .forms import SelfassesmentCreationForm, SelfassesmentChangeForm, SelfassesmentDeleteForm
from .forms import SelfassesmentAccountSubmissionCreationForm, SelfassesmentAccountSubmissionChangeForm, SelfassesmentAccountSubmissionDeleteForm
from .forms import Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form
from .forms import SelfassesmentTrackerCreationForm, SelfassesmentTrackerChangeForm

#models
from .models import Selfassesment, SelfassesmentAccountSubmission
from .models import SelfassesmentTracker

#queries
from .queries import db_search_Selfassesment, db_all_Selfassesment
from .queries import db_search_SelfassesmentAccountSubmission, db_all_SelfassesmentAccountSubmission
from .queries import db_search_SelfassesmentTracker, db_all_SelfassesmentTrackers

from .url_variables import application_name, Selfassesment_name, Selfassesment_path, Selfassesment_Account_Submission_name, Selfassesment_Account_Submission_path
from .url_variables import Limited_name, Limited_Account_Submission_name, SelfassesmentTracker_name
from .url_variables import home_suffix, viewall_suffix, create_suffix, update_suffix, delete_suffix, search_suffix


# html generator
from .html_generator import get_field_names_from_model, generate_template_tag_for_model, generate_data_container_table

# these path names will be passed to templates to use in the navbar links
URL_path_names = {
  'home': f'{application_name}:home',
  
  'selfassesment_home': f'{application_name}:{Selfassesment_name}_{home_suffix}',
  'selfassesment_create': f'{application_name}:{Selfassesment_name}_{create_suffix}',
  'selfassesment_update': f'{application_name}:{Selfassesment_name}_{update_suffix}',
  'selfassesment_update_url_without_argument': f'/{application_name}/{Selfassesment_path}/{update_suffix}/',
  'selfassesment_delete': f'{application_name}:{Selfassesment_name}_{delete_suffix}',
  'selfassesment_delete_url_without_argument': f'/{application_name}/{Selfassesment_path}/{delete_suffix}/',
  'selfassesment_search': f'{application_name}:{Selfassesment_name}_{search_suffix}', # fetch only
  'selfassesment_search_url_without_argument': f'/{application_name}/{Selfassesment_path}/{search_suffix}/', # fetch only
  'selfassesment_viewall': f'{application_name}:{Selfassesment_name}_{viewall_suffix}', # fetch only
  'selfassesment_viewall_url': f'/{application_name}/{Selfassesment_path}/{viewall_suffix}/', # fetch only

  'selfassesment_account_submission_home': f'{application_name}:{Selfassesment_Account_Submission_name}_{home_suffix}',
  'selfassesment_account_submission_create': f'{application_name}:{Selfassesment_Account_Submission_name}_{create_suffix}',
  'selfassesment_account_submission_update': f'{application_name}:{Selfassesment_Account_Submission_name}_{update_suffix}',
  'selfassesment_account_submission_update_url_without_argument': f'/{application_name}/{Selfassesment_Account_Submission_path}/{update_suffix}/',
  'selfassesment_account_submission_delete': f'{application_name}:{Selfassesment_Account_Submission_name}_{delete_suffix}',
  'selfassesment_account_submission_delete_url_without_argument': f'/{application_name}/{Selfassesment_Account_Submission_path}/{delete_suffix}/',
  'selfassesment_account_submission_search': f'{application_name}:{Selfassesment_Account_Submission_name}_{search_suffix}', # fetch only
  'selfassesment_account_submission_search_url_without_argument': f'/{application_name}/{Selfassesment_Account_Submission_path}/{search_suffix}/', # fetch only
  'selfassesment_account_submission_viewall': f'{application_name}:{Selfassesment_Account_Submission_name}_{viewall_suffix}', # fetch only
  'selfassesment_account_submission_viewall_url': f'/{application_name}/{Selfassesment_Account_Submission_path}/{viewall_suffix}/', # fetch only
  'add_all_selfassesment_to_selfassesment_account_submission': f'{application_name}:add_all_{Selfassesment_name}_to_{Selfassesment_Account_Submission_name}',
}

# =============================================================================================================
# =============================================================================================================
# Selfassesment
@login_required
def home_selfassesment(request):
  context = {
    **URL_path_names,
    'model_fields': get_field_names_from_model(Selfassesment),
    'template_tag': generate_template_tag_for_model(Selfassesment, 'client_id'),
    'data_container': generate_data_container_table(Selfassesment, 'client_id'),
  }
  return render(request=request, template_name='companies/selfassesment/home.html', context=context)

@login_required
def view_selfassesment(request):
  return redirect(URL_path_names['selfassesment_home'])

@login_required
def create_selfassesment(request):
  context = {
    **URL_path_names,
  }
  context['form'] = SelfassesmentCreationForm(initial={'client_file_number': Selfassesment.get_next_file_number()})

  if request.method == 'POST':
    form = SelfassesmentCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.set_defaults()
      assesment.created_by = request.user
      assesment.save()
      messages.success(request, f'New Selfassesment has been created with id {assesment.client_id}!')
      return redirect(URL_path_names['selfassesment_home'])
  return render(request, template_name='companies/selfassesment/create.html', context=context)

@login_required
def update_selfassesment(request, client_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = SelfassesmentChangeForm()
  context['client_id'] = client_id

  try:
    record =  Selfassesment.objects.get(client_id=client_id)
    context['form'] = SelfassesmentChangeForm(instance=record)
  except Selfassesment.DoesNotExist:
    messages.error(request, f'Selfassesment Account having id {client_id} does not exists!')
    return redirect(URL_path_names['selfassesment_home'])
    raise Http404

  if request.method == 'POST':
    form = SelfassesmentChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      messages.success(request, f'Selfassesment has been updated having id {client_id}!')
      return redirect(URL_path_names['selfassesment_home'])
    messages.error(request, f'Updating Selfassesment {client_id} failed due to invalid data!')
  return render(request, template_name='companies/selfassesment/update.html', context=context)

@login_required
def delete_selfassesment(request, client_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = SelfassesmentDeleteForm()
  context['client_id'] = client_id

  if request.method == 'POST':
    form = SelfassesmentDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      try:
        record =  Selfassesment.objects.get(client_id=client_id)
        record.delete()
        messages.success(request, f'Selfassesment has been deleted having id {client_id}!')
      except Selfassesment.DoesNotExist:
        messages.error(request, f'Selfassesment record with id {client_id}, you are looking for does not exist!')
    else:
      messages.error(request, f'Deletion of Selfassesment having id {client_id} failed')
    return redirect(URL_path_names['selfassesment_home'])
  return render(request, template_name='companies/selfassesment/delete.html', context=context)

@login_required
def search_selfassesment(request, search_text: str='', limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    if search_text.strip()=='':
      return redirect(URL_path_names['selfassesment_viewall'])
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


# =============================================================================================================
# =============================================================================================================
# SelfassesmentAccountSubmission
@login_required
def home_selfassesment_account_submission(request):
  context = {
    **URL_path_names,
    'model_fields': get_field_names_from_model(SelfassesmentAccountSubmission),
    'template_tag': generate_template_tag_for_model(SelfassesmentAccountSubmission, 'submission_id'),
    'data_container': generate_data_container_table(SelfassesmentAccountSubmission, 'submission_id'),
  }
  return render(request=request, template_name='companies/selfassesment_account_submission/home.html', context=context)

# @login_required
# def view_selfassesment_account_submission(request):
#   return redirect(URL_path_names['selfassesment_account_submission_home'])

@login_required
def create_selfassesment_account_submission(request):
  context = {
    **URL_path_names,
  }
  context['form'] = SelfassesmentAccountSubmissionCreationForm(initial={'submitted_by': request.user.user_id})

  if request.method == 'POST':
    form = SelfassesmentAccountSubmissionCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      if not assesment.submitted_by:
        assesment.submitted_by = request.user
      assesment.set_defaults()
      messages.success(request, f'New Selfassesment Account Submission has been created with id {assesment.submission_id}!')
      return redirect(URL_path_names['selfassesment_account_submission_home'])
  return render(request, template_name='companies/selfassesment_account_submission/create.html', context=context)

@login_required
def update_selfassesment_account_submission(request, submission_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = SelfassesmentAccountSubmissionChangeForm()
  context['submission_id'] = submission_id

  try:
    record =  SelfassesmentAccountSubmission.objects.get(submission_id=submission_id)
    context['form'] = SelfassesmentAccountSubmissionChangeForm(instance=record)
  except SelfassesmentAccountSubmission.DoesNotExist:
    messages.error(request, f'Selfassesment Account Submission having id {submission_id} does not exists!')
    return redirect(URL_path_names['selfassesment_account_submission_home'])
    raise Http404

  if request.method == 'POST':
    form = SelfassesmentAccountSubmissionChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      messages.success(request, f'Selfassesment Account Submission has been updated having id {submission_id}!')
      return redirect(URL_path_names['selfassesment_account_submission_home'])
    messages.error(request, f'Updating Selfassesment Account Submission having id {submission_id} failed due to invalid data!')
  return render(request, template_name='companies/selfassesment_account_submission/update.html', context=context)

@login_required
def delete_selfassesment_account_submission(request, submission_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = SelfassesmentAccountSubmissionDeleteForm()
  context['submission_id'] = submission_id

  if request.method == 'POST':
    form = SelfassesmentAccountSubmissionDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      try:
        record =  SelfassesmentAccountSubmission.objects.get(submission_id=submission_id)
        record.delete()
        messages.success(request, f'Selfassesment Account Submission has been deleted having id {submission_id}!')
      except SelfassesmentAccountSubmission.DoesNotExist:
        messages.error(request, f'Selfassesment Account Submission record with id {submission_id}, you are looking for does not exist!')
        return redirect(URL_path_names['selfassesment_account_submission_home'])
    else:
      messages.error(request, f'Deletion of Selfassesment Account Submission having id {submission_id} failed')
    return redirect(URL_path_names['selfassesment_account_submission_home'])
  return render(request, template_name='companies/selfassesment_account_submission/delete.html', context=context)

@login_required
def search_selfassesment_account_submission(request, search_text: str='', limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    if search_text.strip()=='':
      return redirect(URL_path_names['selfassesment_account_submission_viewall'])
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
    **URL_path_names,
  }
  if not request.user.is_superuser:
    messages.error(request, 'Only Superusers can use this feature!')
    return redirect(URL_path_names['selfassesment_account_submission_home'])
  context['form'] = Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form(initial={'submitted_by': request.user, 'account_prepared_by': request.user})

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
      return redirect(URL_path_names['selfassesment_account_submission_home'])
  return render(request, 'companies/selfassesment_account_submission/add_all_selfassesment_account_submission.html', context=context)


# =============================================================================================================
# =============================================================================================================
# SelfassesmentAccountSubmission
