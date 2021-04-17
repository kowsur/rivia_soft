from django.http.response import Http404, HttpResponse
from django.core.serializers import serialize
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#forms
from .forms import SelfassesmentCreationForm, SelfassesmentChangeForm, SelfassesmentDeleteForm
from .forms import SelfassesmentAccountSubmissionCreationForm, SelfassesmentAccountSubmissionChangeForm
from .forms import Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form
from .forms import TrackerCreationForm, TrackerChangeForm

#models
from .models import Selfassesment, SelfassesmentAccountSubmission
from .models import Tracker

#queries
from .queries import db_search_Selfassesment, db_all_Selfassesment
from .queries import db_search_SelfassesmentAccountSubmission, db_all_SelfassesmentAccountSubmission
from .queries import db_search_Tracker, db_all_Trackers

from .url_variables import application_name, Selfassesment_name, Selfassesment_Account_Submission_name
from .url_variables import Limited_name, Limited_Account_Submission_name, Tracker_name
from .url_variables import home_suffix, viewall_suffix, create_suffix, update_suffix, delete_suffix, search_suffix

# these path names will be passed to templates to use in the navbar links
URL_path_names = {
  'selfassesment_home': f'{application_name}:{Selfassesment_name}_{home_suffix}',
  'selfassesment_create': f'{application_name}:{Selfassesment_name}_{create_suffix}',
  'selfassesment_update': f'{application_name}:{Selfassesment_name}_{update_suffix}',
  'selfassesment_delete': f'{application_name}:{Selfassesment_name}_{delete_suffix}',
  'selfassesment_search': f'{application_name}:{Selfassesment_name}_{search_suffix}', # fetch only
  'selfassesment_viewall': f'{application_name}:{Selfassesment_name}_{viewall_suffix}', # fetch only

  'selfassesment_account_submission_home': f'{application_name}:{Selfassesment_Account_Submission_name}_{home_suffix}',
  'selfassesment_account_submission_create': f'{application_name}:{Selfassesment_Account_Submission_name}_{create_suffix}',
  'selfassesment_account_submission_update': f'{application_name}:{Selfassesment_Account_Submission_name}_{update_suffix}',
  'selfassesment_account_submission_delete': f'{application_name}:{Selfassesment_Account_Submission_name}_{delete_suffix}',
  'selfassesment_account_submission_search': f'{application_name}:{Selfassesment_Account_Submission_name}_{search_suffix}', # fetch only
  'selfassesment_account_submission_viewall': f'{application_name}:{Selfassesment_Account_Submission_name}_{viewall_suffix}', # fetch only
}

# =============================================================================================================
# =============================================================================================================
# Selfassesment
@login_required
def view_selfassesment(request):
  context = {
    **URL_path_names,
  }
  return render(request=request, template_name='companies/selfassesment/home.html', context=context)

@login_required
def home_selfassesment(request):
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
      messages.success(request, 'New Selfassesment has been created!')
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
    raise Http404

  if request.method == 'POST':
    form = SelfassesmentCreationForm(request.POST, instance=record)
    context['form'] = form
    if form.is_valid():
      assesment = form.save()
      messages.success(request, f'Selfassesment has been updated having id {client_id}!')
      return redirect(URL_path_names['selfassesment_home'])
    messages.error(request, 'Update failed due to invalid data!')
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
        messages.error(request, f'The record having id {client_id}, you are looking for does not exist!')
      return redirect(URL_path_names['selfassesment_home'])
  return render(request, template_name='companies/selfassesment/delete.html', context=context)

@login_required
def search_selfassesment(request, search_text: str='', limit: int=-1):
  if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
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


# # =============================================================================================================
# # =============================================================================================================
# # SelfassesmentAccountSubmission
# @login_required
# def view_selfassesment_account_submission(request):
#   context = {
#     **URL_path_names,
#   }
#   return render(request=request, template_name='companies/selfassesment/home.html', context=context)

# @login_required
# def home_selfassesment_account_submission(request):
#   return view_selfassesment_account_submission(request)

# @login_required
# def create_selfassesment_account_submission(request):
#   context = {
#     **URL_path_names,
#   }
#   context['form'] = SelfassesmentAccountSubmissionCreationForm()
#   return render(request, template_name='companies/selfassesment/create.html', context=context)

# @login_required
# def update_selfassesment_account_submission(request, client_id:int):
#   context = {
#     **URL_path_names,
#   }
#   context['form'] = SelfassesmentAccountSubmissionChangeForm()
#   return render(request, template_name='companies/selfassesment/update.html', context=context)

# @login_required
# def delete_selfassesment_account_submission(request, client_id:int):
#   context = {
#     **URL_path_names,
#   }
#   context['form'] = SelfassesmentAccountSubmissionChangeForm()
#   return render(request, template_name='companies/selfassesment/delete.html', context=context)

# @login_required
# def search_selfassesment_account_submission(request, search_text: str='', limit: int=-1):
#   if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
#     records = db_search_SelfassesmentAccountSubmission(search_text, limit)
#     data = serialize(queryset=records, format='json')
#     return HttpResponse(data, content_type='application/json')
#   raise Http404

# @login_required
# def all_selfassesment_account_submission(request, limit=-1):
#   if request.method=='GET' and request.headers.get('Content-Type')=='application/json':
#     records = db_all_SelfassesmentAccountSubmission(limit)
#     data = serialize(queryset=records, format='json')
#     return HttpResponse(data, content_type='application/json')
#   raise Http404
