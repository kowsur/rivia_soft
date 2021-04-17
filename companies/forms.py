from django import forms
from .models import Selfassesment, SelfassesmentAccountSubmission, Tracker
from django.utils import timezone


class SelfassesmentCreationForm(forms.ModelForm):
    date_of_registration = forms.DateField(
        label='Registration date',
        widget=forms.DateInput(attrs={'type': 'date', 'value': timezone.localdate(), 'placehoder': 'Registration date'})
    )

    class Meta:
        model = Selfassesment
        fields = (
            # 'client_id',
            'client_file_number', 
            'client_name', 
            'client_phone_number', 
            'date_of_registration', 
            'UTR', 
            'HMRC_referance', 
            'NINO', 
            'gateway_id', 
            'gateway_password', 
            'address', 
            'post_code', 
            'email', 
            'bank_name', 
            'bank_account_number', 
            'bank_sort_code', 
            'bank_account_holder_name', 
            'is_active')


class SelfassesmentChangeForm(forms.ModelForm):
    date_of_registration = forms.DateField(
        label='Registration date',
        widget=forms.DateInput(attrs={'type': 'date', 'value': timezone.localdate(), 'placehoder': 'Registration date'})
    )
    
    class Meta:
        model = Selfassesment
        fields = (
            # 'is_updated',
            # 'client_id',
            'client_file_number',
            'client_name',
            'client_phone_number',
            'date_of_registration',
            'UTR',
            'HMRC_referance',
            'NINO',
            'gateway_id',
            'gateway_password',
            'address',
            'post_code',
            'email',
            'bank_name',
            'bank_account_number',
            'bank_sort_code',
            'bank_account_holder_name',
            'is_active')



class SelfassesmentAccountSubmissionCreationForm(forms.ModelForm):
    date_of_submission = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = SelfassesmentAccountSubmission
        fields = (
            # 'is_updated',
            # 'submission_id',
            'client_id',
            'date_of_submission', 
            'tax_year', 
            'submitted_by', 
            'account_prepared_by', 
            'remarks', 
            'paid_amount', 
            'is_paid', 
            'is_submitted')


class SelfassesmentAccountSubmissionChangeForm(forms.ModelForm):
    date_of_submission = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = SelfassesmentAccountSubmission
        fields = (
            # 'submission_id',
            'client_id', 
            'date_of_submission', 
            'tax_year', 
            'submitted_by', 
            'account_prepared_by', 
            'remarks', 
            'paid_amount', 
            'is_paid', 
            'is_submitted')

class Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form(forms.ModelForm):
    date_of_submission = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = SelfassesmentAccountSubmission
        fields = (
            # 'submission_id',
            'tax_year', 
            'submitted_by', 
            'account_prepared_by', 
            'remarks')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tax_year'].required = True


class TrackerCreationForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Tracker
        fields = (
            # 'tracker_id',
            # 'created_by', #request.user
            # 'done_by', #request.user
            'client_id',
            'job_description',
            'deadline', #default timezone.now
            # 'complete_date', #default timezone.now
            # 'is_completed',
            )

class TrackerChangeForm(forms.ModelForm):
    complete_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Tracker
        fields = (
            # 'tracker_id',
            # 'created_by',
            'done_by',
            # 'client_id',
            # 'job_description',
            # 'deadline',
            'complete_date',
            'is_completed',)
