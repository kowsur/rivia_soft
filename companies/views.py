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
from .forms import SelfassesmentTrackerCreationForm, SelfassesmentTrackerChangeForm, SelfassesmentTrackerDeleteForm

from .forms import LimitedCreationForm, LimitedChangeForm, LimitedDeleteForm
from .forms import LimitedAccountSubmissionCreationForm, LimitedAccountSubmissionChangeForm, LimitedAccountSubmissionDeleteForm
from .forms import LimitedTrackerCreationForm, LimitedTrackerChangeForm, LimitedTrackerDeleteForm
from .forms import Add_All_Limited_to_LimitedAccountSubmission_Form

#models
from .models import Selfassesment, SelfassesmentAccountSubmission
from .models import SelfassesmentTracker
from .models import Limited, LimitedAccountSubmission, LimitedTracker

#queries
from .queries import db_search_Selfassesment, db_all_Selfassesment
from .queries import db_search_SelfassesmentAccountSubmission, db_all_SelfassesmentAccountSubmission
from .queries import db_search_SelfassesmentTracker, db_all_SelfassesmentTracker

from .queries import db_search_Limited, db_all_Limited
from .queries import db_search_LimitedAccountSubmission, db_all_LimitedAccountSubmission
from .queries import db_search_LimitedTracker, db_all_LimitedTracker


from .url_variables import *


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

  'selfassesment_tracker_home': f'{application_name}:{SelfassesmentTracker_name}_{home_suffix}',
  'selfassesment_tracker_create': f'{application_name}:{SelfassesmentTracker_name}_{create_suffix}',
  'selfassesment_tracker_update': f'{application_name}:{SelfassesmentTracker_name}_{update_suffix}',
  'selfassesment_tracker_update_url_without_argument': f'/{application_name}/{SelfassesmentTracker_path}/{update_suffix}/',
  'selfassesment_tracker_delete': f'{application_name}:{SelfassesmentTracker_name}_{delete_suffix}',
  'selfassesment_tracker_delete_url_without_argument': f'/{application_name}/{SelfassesmentTracker_path}/{delete_suffix}/',
  'selfassesment_tracker_search': f'{application_name}:{SelfassesmentTracker_name}_{search_suffix}', # fetch only
  'selfassesment_tracker_search_url_without_argument': f'/{application_name}/{SelfassesmentTracker_path}/{search_suffix}/', # fetch only
  'selfassesment_tracker_viewall': f'{application_name}:{SelfassesmentTracker_name}_{viewall_suffix}', # fetch only
  'selfassesment_tracker_viewall_url': f'/{application_name}/{SelfassesmentTracker_path}/{viewall_suffix}/', # fetch only
  
  
  'limited_home': f'{application_name}:{Limited_name}_{home_suffix}',
  'limited_create': f'{application_name}:{Limited_name}_{create_suffix}',
  'limited_update': f'{application_name}:{Limited_name}_{update_suffix}',
  'limited_update_url_without_argument': f'/{application_name}/{Limited_path}/{update_suffix}/',
  'limited_delete': f'{application_name}:{Limited_name}_{delete_suffix}',
  'limited_delete_url_without_argument': f'/{application_name}/{Limited_path}/{delete_suffix}/',
  'limited_search': f'{application_name}:{Limited_name}_{search_suffix}', # fetch only
  'limited_search_url_without_argument': f'/{application_name}/{Limited_path}/{search_suffix}/', # fetch only
  'limited_viewall': f'{application_name}:{Limited_name}_{viewall_suffix}', # fetch only
  'limited_viewall_url': f'/{application_name}/{Limited_path}/{viewall_suffix}/', # fetch only

  'limited_account_submission_home': f'{application_name}:{Limited_Account_Submission_name}_{home_suffix}',
  'limited_account_submission_create': f'{application_name}:{Limited_Account_Submission_name}_{create_suffix}',
  'limited_account_submission_update': f'{application_name}:{Limited_Account_Submission_name}_{update_suffix}',
  'limited_account_submission_update_url_without_argument': f'/{application_name}/{Limited_Account_Submission_path}/{update_suffix}/',
  'limited_account_submission_delete': f'{application_name}:{Limited_Account_Submission_name}_{delete_suffix}',
  'limited_account_submission_delete_url_without_argument': f'/{application_name}/{Limited_Account_Submission_path}/{delete_suffix}/',
  'limited_account_submission_search': f'{application_name}:{Limited_Account_Submission_name}_{search_suffix}', # fetch only
  'limited_account_submission_search_url_without_argument': f'/{application_name}/{Limited_Account_Submission_path}/{search_suffix}/', # fetch only
  'limited_account_submission_viewall': f'{application_name}:{Limited_Account_Submission_name}_{viewall_suffix}', # fetch only
  'limited_account_submission_viewall_url': f'/{application_name}/{Limited_Account_Submission_path}/{viewall_suffix}/', # fetch only
  'add_all_limited_to_limited_account_submission': f'{application_name}:add_all_{Limited_name}_to_{Limited_Account_Submission_name}',

  'limited_tracker_home': f'{application_name}:{LimitedTracker_name}_{home_suffix}',
  'limited_tracker_create': f'{application_name}:{LimitedTracker_name}_{create_suffix}',
  'limited_tracker_update': f'{application_name}:{LimitedTracker_name}_{update_suffix}',
  'limited_tracker_update_url_without_argument': f'/{application_name}/{LimitedTracker_path}/{update_suffix}/',
  'limited_tracker_delete': f'{application_name}:{LimitedTracker_name}_{delete_suffix}',
  'limited_tracker_delete_url_without_argument': f'/{application_name}/{LimitedTracker_path}/{delete_suffix}/',
  'limited_tracker_search': f'{application_name}:{LimitedTracker_name}_{search_suffix}', # fetch only
  'limited_tracker_search_url_without_argument': f'/{application_name}/{LimitedTracker_path}/{search_suffix}/', # fetch only
  'limited_tracker_viewall': f'{application_name}:{LimitedTracker_name}_{viewall_suffix}', # fetch only
  'limited_tracker_viewall_url': f'/{application_name}/{LimitedTracker_path}/{viewall_suffix}/', # fetch only
}

# =============================================================================================================
# =============================================================================================================
# Selfassesment
@login_required
def home_selfassesment(request):
  pk_field = 'client_id'
  exclude_fields = set(['client_id', 'is_updated', 'created_by'])
  context = {
    **URL_path_names,
    'model_fields': get_field_names_from_model(Selfassesment),
    'template_tag': generate_template_tag_for_model(Selfassesment, pk_filed=pk_field, exclude_fields=exclude_fields),
    'data_container': generate_data_container_table(Selfassesment, pk_filed=pk_field, exclude_fields=exclude_fields),
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
  pk_field = 'submission_id'
  exclude_fields = set(['submission_id', 'is_updated', 'created_by'])
  context = {
    **URL_path_names,
    'model_fields': get_field_names_from_model(SelfassesmentAccountSubmission),
    'template_tag': generate_template_tag_for_model(SelfassesmentAccountSubmission, pk_filed=pk_field, exclude_fields=exclude_fields),
    'data_container': generate_data_container_table(SelfassesmentAccountSubmission, pk_filed=pk_field, exclude_fields=exclude_fields),
  }
  return render(request=request, template_name='companies/selfassesment_account_submission/home.html', context=context)

@login_required
def view_selfassesment_account_submission(request):
  return redirect(URL_path_names['selfassesment_account_submission_home'])

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
# SelfassesmentTracker
@login_required
def home_selfassesment_tracker(request):
  pk_field = 'tracker_id'
  exclude_fields = set(['tracker_id', 'is_updated', 'creation_date'])
  context = {
    **URL_path_names,
    'model_fields': get_field_names_from_model(SelfassesmentTracker),
    'template_tag': generate_template_tag_for_model(SelfassesmentTracker, pk_filed=pk_field, exclude_fields=exclude_fields),
    'data_container': generate_data_container_table(SelfassesmentTracker, pk_filed=pk_field, exclude_fields=exclude_fields),
  }
  return render(request=request, template_name='companies/selfassesment_tracker/home.html', context=context)

@login_required
def view_selfassesment_tracker(request):
  return redirect(URL_path_names['selfassesment_tracker_home'])

@login_required
def create_selfassesment_tracker(request):
  context = {
    **URL_path_names,
  }
  context['form'] = SelfassesmentTrackerCreationForm(initial={'created_by': request.user.user_id})

  if request.method == 'POST':
    form = SelfassesmentTrackerCreationForm(request.POST, initial={'created_by': request.user.user_id})
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.created_by = request.user
      assesment.done_by = request.user
      assesment.save()
      messages.success(request, f'New Selfassesment Tracker has been created with id {assesment.tracker_id}!')
      return redirect(URL_path_names['selfassesment_tracker_home'])
  return render(request, template_name='companies/selfassesment_tracker/create.html', context=context)

@login_required
def update_selfassesment_tracker(request, tracker_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = SelfassesmentTrackerChangeForm()
  context['tracker_id'] = tracker_id

  try:
    record =  SelfassesmentTracker.objects.get(tracker_id=tracker_id)
    context['form'] = SelfassesmentTrackerChangeForm(instance=record)
  except SelfassesmentTracker.DoesNotExist:
    messages.error(request, f'Selfassesment Tracker having id {tracker_id} does not exists!')
    return redirect(URL_path_names['selfassesment_tracker_home'])
    raise Http404

  if request.method == 'POST':
    form = SelfassesmentTrackerChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      messages.success(request, f'Selfassesment Tracker has been updated having id {tracker_id}!')
      return redirect(URL_path_names['selfassesment_tracker_home'])
    messages.error(request, f'Updating Selfassesment Tracker having id {tracker_id} failed due to invalid data!')
  return render(request, template_name='companies/selfassesment_tracker/update.html', context=context)

@login_required
def delete_selfassesment_tracker(request, tracker_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = SelfassesmentTrackerDeleteForm()
  context['tracker_id'] = tracker_id

  if request.method == 'POST':
    form = SelfassesmentTrackerDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      try:
        record =  SelfassesmentTracker.objects.get(tracker_id=tracker_id)
        record.delete()
        messages.success(request, f'Selfassesment Tracker has been deleted having id {tracker_id}!')
      except SelfassesmentTracker.DoesNotExist:
        messages.error(request, f'Selfassesment Tracker record with id {tracker_id}, you are looking for does not exist!')
        return redirect(URL_path_names['selfassesment_tracker_home'])
    else:
      messages.error(request, f'Deletion of Selfassesment Tracker having id {tracker_id} failed')
    return redirect(URL_path_names['selfassesment_tracker_home'])
  return render(request, template_name='companies/selfassesment_tracker/delete.html', context=context)

@login_required
def search_selfassesment_tracker(request, search_text: str='', limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    if search_text.strip()=='':
      return redirect(URL_path_names['selfassesment_tracker_viewall'])
    records = db_search_SelfassesmentTracker(search_text, limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_selfassesment_tracker(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_SelfassesmentTracker(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404



# =============================================================================================================
# =============================================================================================================
# Limited
@login_required
def home_limited(request):
  pk_field = 'client_id'
  exclude_fields = set(['client_id', 'is_updated', 'created_by'])
  context = {
    **URL_path_names,
    'model_fields': get_field_names_from_model(Limited),
    'template_tag': generate_template_tag_for_model(Limited, pk_filed=pk_field, exclude_fields=exclude_fields),
    'data_container': generate_data_container_table(Limited, pk_filed=pk_field, exclude_fields=exclude_fields),
  }
  return render(request=request, template_name='companies/limited/home.html', context=context)

@login_required
def view_limited(request):
  return redirect(URL_path_names['limited_home'])

@login_required
def create_limited(request):
  context = {
    **URL_path_names,
  }
  context['form'] = LimitedCreationForm(initial={'client_file_number': Limited.get_next_file_number()})

  if request.method == 'POST':
    form = LimitedCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.set_defaults()
      assesment.created_by = request.user
      assesment.save()
      messages.success(request, f'New Limited has been created with id {assesment.client_id}!')
      return redirect(URL_path_names['limited_home'])
  return render(request, template_name='companies/limited/create.html', context=context)

@login_required
def update_limited(request, client_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = LimitedChangeForm()
  context['client_id'] = client_id

  try:
    record =  Limited.objects.get(client_id=client_id)
    context['form'] = LimitedChangeForm(instance=record)
  except Limited.DoesNotExist:
    messages.error(request, f'Limited Account having id {client_id} does not exists!')
    return redirect(URL_path_names['limited_home'])
    raise Http404

  if request.method == 'POST':
    form = LimitedChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      messages.success(request, f'Limited has been updated having id {client_id}!')
      return redirect(URL_path_names['limited_home'])
    messages.error(request, f'Updating Limited {client_id} failed due to invalid data!')
  return render(request, template_name='companies/limited/update.html', context=context)

@login_required
def delete_limited(request, client_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = LimitedDeleteForm()
  context['client_id'] = client_id

  if request.method == 'POST':
    form = LimitedDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      try:
        record =  Limited.objects.get(client_id=client_id)
        record.delete()
        messages.success(request, f'Limited has been deleted having id {client_id}!')
      except Limited.DoesNotExist:
        messages.error(request, f'Limited record with id {client_id}, you are looking for does not exist!')
    else:
      messages.error(request, f'Deletion of Limited having id {client_id} failed')
    return redirect(URL_path_names['limited_home'])
  return render(request, template_name='companies/limited/delete.html', context=context)

@login_required
def search_limited(request, search_text: str='', limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    if search_text.strip()=='':
      return redirect(URL_path_names['limited_viewall'])
    records = db_search_Limited(search_text, limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_limited(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_Limited(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404


# =============================================================================================================
# =============================================================================================================
# LimitedAccountSubmission
@login_required
def home_limited_account_submission(request):
  pk_field = 'submission_id'
  exclude_fields = set(['submission_id', 'is_updated', 'created_by'])
  context = {
    **URL_path_names,
    'model_fields': get_field_names_from_model(LimitedAccountSubmission),
    'template_tag': generate_template_tag_for_model(LimitedAccountSubmission, pk_filed=pk_field, exclude_fields=exclude_fields),
    'data_container': generate_data_container_table(LimitedAccountSubmission, pk_filed=pk_field, exclude_fields=exclude_fields),
  }
  return render(request=request, template_name='companies/limited_account_submission/home.html', context=context)

@login_required
def view_limited_account_submission(request):
  return redirect(URL_path_names['limited_account_submission_home'])

@login_required
def create_limited_account_submission(request):
  context = {
    **URL_path_names,
  }
  context['form'] = LimitedAccountSubmissionCreationForm(initial={'submitted_by': request.user.user_id})

  if request.method == 'POST':
    form = LimitedAccountSubmissionCreationForm(request.POST)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      if not assesment.submitted_by:
        assesment.submitted_by = request.user
      assesment.set_defaults()
      messages.success(request, f'New Limited Account Submission has been created with id {assesment.submission_id}!')
      return redirect(URL_path_names['limited_account_submission_home'])
  return render(request, template_name='companies/limited_account_submission/create.html', context=context)

@login_required
def update_limited_account_submission(request, submission_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = LimitedAccountSubmissionChangeForm()
  context['submission_id'] = submission_id

  try:
    record =  LimitedAccountSubmission.objects.get(submission_id=submission_id)
    context['form'] = LimitedAccountSubmissionChangeForm(instance=record)
  except LimitedAccountSubmission.DoesNotExist:
    messages.error(request, f'Limited Account Submission having id {submission_id} does not exists!')
    return redirect(URL_path_names['limited_account_submission_home'])
    raise Http404

  if request.method == 'POST':
    form = LimitedAccountSubmissionChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      messages.success(request, f'Limited Account Submission has been updated having id {submission_id}!')
      return redirect(URL_path_names['limited_account_submission_home'])
    messages.error(request, f'Updating Limited Account Submission having id {submission_id} failed due to invalid data!')
  return render(request, template_name='companies/limited_account_submission/update.html', context=context)

@login_required
def delete_limited_account_submission(request, submission_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = LimitedAccountSubmissionDeleteForm()
  context['submission_id'] = submission_id

  if request.method == 'POST':
    form = LimitedAccountSubmissionDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      try:
        record =  LimitedAccountSubmission.objects.get(submission_id=submission_id)
        record.delete()
        messages.success(request, f'Limited Account Submission has been deleted having id {submission_id}!')
      except LimitedAccountSubmission.DoesNotExist:
        messages.error(request, f'Limited Account Submission record with id {submission_id}, you are looking for does not exist!')
        return redirect(URL_path_names['limited_account_submission_home'])
    else:
      messages.error(request, f'Deletion of Limited Account Submission having id {submission_id} failed')
    return redirect(URL_path_names['limited_account_submission_home'])
  return render(request, template_name='companies/limited_account_submission/delete.html', context=context)

@login_required
def search_limited_account_submission(request, search_text: str='', limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    if search_text.strip()=='':
      return redirect(URL_path_names['limited_account_submission_viewall'])
    records = db_search_LimitedAccountSubmission(search_text, limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_limited_account_submission(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_LimitedAccountSubmission(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

# add_all_limited_to_limited_account_submission_w_submission_year
@login_required
def add_all_limited_to_limited_account_submission_w_submission_year(request):
  context = {
    **URL_path_names,
  }
  if not request.user.is_superuser:
    messages.error(request, 'Only Superusers can use this feature!')
    return redirect(URL_path_names['limited_account_submission_home'])
  context['form'] = Add_All_Limited_to_LimitedAccountSubmission_Form(initial={'submitted_by': request.user, 'account_prepared_by': request.user})

  if request.method=='POST':
    form = Add_All_Limited_to_LimitedAccountSubmission_Form(data=request.POST)
    context['form'] = form
    if form.is_valid():
      submitted_by = form.cleaned_data.get('submitted_by')
      if submitted_by==None:
        form.cleaned_data['submitted_by'] = request.user

      all_Limiteds = Limited.objects.all()
      
      for assesment in all_Limiteds:
        form.cleaned_data['client_id'] = assesment
        instance = LimitedAccountSubmission(**form.cleaned_data)
        instance.set_defaults()
        instance.save()
      messages.success(request, 'Added all Limited to Limited Account Submission!')
      return redirect(URL_path_names['limited_account_submission_home'])
  return render(request, 'companies/limited_account_submission/add_all_limited_account_submission.html', context=context)


# =============================================================================================================
# =============================================================================================================
# LimitedTracker
@login_required
def home_limited_tracker(request):
  pk_field = 'tracker_id'
  exclude_fields = set(['tracker_id', 'is_updated', 'creation_date'])
  context = {
    **URL_path_names,
    'model_fields': get_field_names_from_model(LimitedTracker),
    'template_tag': generate_template_tag_for_model(LimitedTracker, pk_filed=pk_field, exclude_fields=exclude_fields),
    'data_container': generate_data_container_table(LimitedTracker, pk_filed=pk_field, exclude_fields=exclude_fields),
  }
  return render(request=request, template_name='companies/limited_tracker/home.html', context=context)

@login_required
def view_limited_tracker(request):
  return redirect(URL_path_names['limited_tracker_home'])

@login_required
def create_limited_tracker(request):
  context = {
    **URL_path_names,
  }
  context['form'] = LimitedTrackerCreationForm(initial={'created_by': request.user.user_id})

  if request.method == 'POST':
    form = LimitedTrackerCreationForm(request.POST, initial={'created_by': request.user.user_id})
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      assesment.created_by = request.user
      assesment.done_by = request.user
      assesment.save()
      messages.success(request, f'New Limited Tracker has been created with id {assesment.tracker_id}!')
      return redirect(URL_path_names['limited_tracker_home'])
  return render(request, template_name='companies/limited_tracker/create.html', context=context)

@login_required
def update_limited_tracker(request, tracker_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = LimitedTrackerChangeForm()
  context['tracker_id'] = tracker_id

  try:
    record =  LimitedTracker.objects.get(tracker_id=tracker_id)
    context['form'] = LimitedTrackerChangeForm(instance=record)
  except LimitedTracker.DoesNotExist:
    messages.error(request, f'Limited Tracker having id {tracker_id} does not exists!')
    return redirect(URL_path_names['limited_tracker_home'])
    raise Http404

  if request.method == 'POST':
    form = LimitedTrackerChangeForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      messages.success(request, f'Limited Tracker has been updated having id {tracker_id}!')
      return redirect(URL_path_names['limited_tracker_home'])
    messages.error(request, f'Updating Limited Tracker having id {tracker_id} failed due to invalid data!')
  return render(request, template_name='companies/limited_tracker/update.html', context=context)

@login_required
def delete_limited_tracker(request, tracker_id:int):
  context = {
    **URL_path_names,
  }
  context['form'] = LimitedTrackerDeleteForm()
  context['tracker_id'] = tracker_id

  if request.method == 'POST':
    form = LimitedTrackerDeleteForm(request.POST)
    context['form'] = form
    if form.is_valid():
      try:
        record =  LimitedTracker.objects.get(tracker_id=tracker_id)
        record.delete()
        messages.success(request, f'Limited Tracker has been deleted having id {tracker_id}!')
      except LimitedTracker.DoesNotExist:
        messages.error(request, f'Limited Tracker record with id {tracker_id}, you are looking for does not exist!')
        return redirect(URL_path_names['limited_tracker_home'])
    else:
      messages.error(request, f'Deletion of Limited Tracker having id {tracker_id} failed')
    return redirect(URL_path_names['limited_tracker_home'])
  return render(request, template_name='companies/limited_tracker/delete.html', context=context)

@login_required
def search_limited_tracker(request, search_text: str='', limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    if search_text.strip()=='':
      return redirect(URL_path_names['limited_tracker_viewall'])
    records = db_search_LimitedTracker(search_text, limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404

@login_required
def all_limited_tracker(request, limit=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
    records = db_all_LimitedTracker(limit)
    data = serialize(queryset=records, format='json')
    return HttpResponse(data, content_type='application/json')
  raise Http404
