from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Selfassesment, SelfassesmentAccountSubmission, SelfassesmentTracker
from django.core.exceptions import ValidationError
from django.utils import timezone
from .fields import SearchableModelField, Select, Fieldset
from .url_variables import Full_URL_PATHS_WITHOUT_ARGUMENTS

# dummy import
# next line before migrating
# from .dummy_class import *


from users.models import CustomUser
search_users_url_path = '/u/search/'
all_users_url_path = '/u/all/'

Selfassesment_client_id_repr_format = r"👥{fields.client_name} 📁{fields.client_file_number} 📞{fields.personal_phone_number} ☎{fields.business_phone_number}"
CustomUser_repr_format = r"📨{fields.email} 👥{fields.first_name}"


def get_date_today(date_format = '%Y-%m-%d'):
    today = timezone.datetime.strftime(timezone.now(), date_format)
    return today

class SelfassesmentCreationForm(forms.ModelForm):
    date_of_registration = forms.DateField(
        label='Registration date',
        widget=forms.DateInput(attrs={'type': 'date', 'value': get_date_today, 'placehoder': 'Registration date'})
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date',})
    )

    class Meta:
        model = Selfassesment
        fields = (
            # 'client_id',
            # 'created_by',
            # 'is_updated',
            'selfassesment_type',
            'date_of_registration',
            'is_active',
            'remarks',

            'client_file_number',
            'client_name',

            'date_of_birth',
            'PAYE_number',
            'personal_phone_number',
            'personal_email',
            'personal_address',
            'personal_post_code',

            'AOR_number',
            'business_phone_number',
            'business_email',
            'business_address',
            'business_post_code',

            'HMRC_agent',
            'HMRC_referance',
            'UTR',
            'NINO',
            'gateway_id',
            'gateway_password',
            
            'bank_name',
            'bank_account_number',
            'bank_sort_code',
            'bank_account_holder_name',
            )
        fieldsets = (
            Fieldset(
                title = 'Client Info',
                fields = ('client_file_number', 'selfassesment_type', 'date_of_registration', 'client_name', 'remarks', 'is_active', )
                ),
            Fieldset(
                title = 'Personal Info',
                fields = ('date_of_birth', 'personal_phone_number', 'personal_email', 'personal_address', 'personal_post_code', )
                ),
            Fieldset(
                title = 'HMRC Details',
                fields =  ('HMRC_referance', 'UTR', 'NINO', 'HMRC_agent', 'gateway_id', 'gateway_password', )
            ),
            Fieldset(
                title = 'Business Info', 
                fields = ('business_phone_number', 'business_email', 'business_address', 'business_post_code', 'PAYE_number', 'AOR_number', )
                ),
            Fieldset(
                title = 'Bank Info',
                fields = ('bank_name', 'bank_account_number', 'bank_sort_code', 'bank_account_holder_name',)
                ),
        )


class SelfassesmentChangeForm(forms.ModelForm):
    date_of_registration = forms.DateField(
        label='Registration date',
        widget=forms.DateInput(attrs={'type': 'date', 'value': get_date_today, 'placehoder': 'Registration date'})
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date',})
    )
    
    class Meta:
        model = Selfassesment
        fields = (
            # 'client_id',
            # 'created_by',
            # 'is_updated',
            'selfassesment_type',
            'date_of_registration',
            'is_active',
            'remarks',

            'client_file_number',
            'client_name',

            'date_of_birth',
            'PAYE_number',
            'personal_phone_number',
            'personal_email',
            'personal_address',
            'personal_post_code',

            'AOR_number',
            'business_phone_number',
            'business_email',
            'business_address',
            'business_post_code',

            'HMRC_agent',
            'HMRC_referance',
            'UTR',
            'NINO',
            'gateway_id',
            'gateway_password',
            
            'bank_name',
            'bank_account_number',
            'bank_sort_code',
            'bank_account_holder_name',
            )
        fieldsets = (
            Fieldset(
                title = 'Client Info',
                fields = ('client_file_number', 'selfassesment_type', 'date_of_registration', 'client_name', 'remarks', 'is_active', )
                ),
            Fieldset(
                title = 'Personal Info',
                fields = ('date_of_birth', 'personal_phone_number', 'personal_email', 'personal_address', 'personal_post_code', )
                ),
            Fieldset(
                title = 'HMRC Details',
                fields =  ('HMRC_referance', 'UTR', 'NINO', 'HMRC_agent', 'gateway_id', 'gateway_password', )
            ),
            Fieldset(
                title = 'Business Info', 
                fields = ('business_phone_number', 'business_email', 'business_address', 'business_post_code', 'PAYE_number', 'AOR_number', )
                ),
            Fieldset(
                title = 'Bank Info',
                fields = ('bank_name', 'bank_account_number', 'bank_sort_code', 'bank_account_holder_name',)
                ),
        )

class SelfassesmentDeleteForm(forms.ModelForm):
    agree = forms.BooleanField(label='I want to proceed.', required=True)
    class Meta:
        model = Selfassesment
        fields = ()


class SelfassesmentAccountSubmissionCreationForm(forms.ModelForm):
    date_of_submission = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'value': get_date_today}))
    client_id = SearchableModelField(
        queryset=Selfassesment.objects.all(),
        label = 'Client Name',
        search_url = Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_search_url,
        all_url = Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_viewall_url,
        repr_format = Selfassesment_client_id_repr_format,
        model=Selfassesment,
        choices=Selfassesment.objects.all().only('client_id', 'client_name'),
        fk_field='client_id',
        empty_label=None
        )

    class Meta:
        model = SelfassesmentAccountSubmission
        fields = (
            # 'is_updated',
            # 'submission_id',
            'client_id',
            'date_of_submission', 
            'tax_year', 
            # 'submitted_by', 
            # 'prepared_by', 
            'remarks', 
            # 'paid_amount', 
            # 'is_paid', 
            # 'is_submitted'
            )
        labels = {
            'client_id': _('Client Name'),
        }


class SelfassesmentAccountSubmissionChangeForm(forms.ModelForm):
    date_of_submission = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    client_id = SearchableModelField(
        queryset=Selfassesment.objects.all(),
        label = 'Client Name',
        search_url = Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_search_url,
        all_url = Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_viewall_url,
        repr_format = Selfassesment_client_id_repr_format,
        model=Selfassesment,
        choices=Selfassesment.objects.all().only('client_id', 'client_name'),
        fk_field='client_id',
        empty_label=None,
        disabled=False
        )
    prepared_by = SearchableModelField(
        queryset=CustomUser.objects.all(),
        search_url = search_users_url_path,
        all_url = all_users_url_path,
        repr_format = CustomUser_repr_format,
        model=CustomUser,
        choices=CustomUser.objects.all().only('user_id', 'first_name'),
        fk_field='user_id',
        empty_label=None,
        disabled=False
        )

    class Meta:
        model = SelfassesmentAccountSubmission
        fields = (
            # 'submission_id',
            'client_id', 
            'date_of_submission', 
            'tax_year', 
            # 'submitted_by', 
            'prepared_by', 
            'remarks', 
            'paid_amount', 
            'is_paid', 
            'is_submitted')
        labels = {
            'client_id': _('Client Name'),
        }

class SelfassesmentAccountSubmissionDeleteForm(forms.ModelForm):
    agree = forms.BooleanField(label='I want to proceed.', required=True)
    class Meta:
        model = SelfassesmentAccountSubmission
        fields = ()


class Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form(forms.ModelForm):
    date_of_submission = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'value': get_date_today}))
    submitted_by = SearchableModelField(
        queryset=CustomUser.objects.all(),
        search_url = search_users_url_path,
        all_url = all_users_url_path,
        repr_format = CustomUser_repr_format,
        model=CustomUser,
        choices=CustomUser.objects.all().only('user_id', 'first_name'),
        fk_field='user_id',
        empty_label=None
        )
    prepared_by = SearchableModelField(
        queryset=CustomUser.objects.all(),
        search_url = search_users_url_path,
        all_url = all_users_url_path,
        repr_format = CustomUser_repr_format,
        model=CustomUser,
        choices=CustomUser.objects.all().only('user_id', 'first_name'),
        fk_field='user_id',
        empty_label=None,
        )
    
    class Meta:
        model = SelfassesmentAccountSubmission
        fields = (
            # 'submission_id',
            'tax_year', 
            'submitted_by', 
            'prepared_by', 
            'remarks',
            'date_of_submission')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tax_year'].required = True


class SelfassesmentTrackerCreationForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'value': get_date_today, 'min': get_date_today}))
    client_id = SearchableModelField(
        queryset=Selfassesment.objects.all(),
        label = 'Client Name',
        search_url = Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_search_url,
        all_url = Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_viewall_url,
        repr_format = Selfassesment_client_id_repr_format,
        model=Selfassesment,
        choices=Selfassesment.objects.all().only('client_id', 'client_name'),
        fk_field='client_id',
        empty_label=None
        )
    
    class Meta:
        model = SelfassesmentTracker
        fields = (
            # 'tracker_id',
            # 'created_by', #request.user
            # 'done_by', #request.user
            'client_id',
            'job_description',
            'remarks',
            'has_issue',
            'deadline', #default timezone now
            # 'complete_date', #default timezone now
            # 'is_completed',
            )
    def clean_deadline(self):
        input_date = self.cleaned_data['deadline']
        current_date = timezone.now().date()
        if input_date>=current_date:
            return input_date
        raise ValidationError("Deadline can't be a previous date.")
        


class SelfassesmentTrackerChangeForm(forms.ModelForm):
    # complete_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    client_id = SearchableModelField(
        queryset=Selfassesment.objects.all(),
        label = 'Client Name',
        search_url = Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_search_url,
        all_url = Full_URL_PATHS_WITHOUT_ARGUMENTS.Selfassesment_viewall_url,
        repr_format = Selfassesment_client_id_repr_format,
        model=Selfassesment,
        choices=Selfassesment.objects.all().only('client_id', 'client_name'),
        fk_field='client_id',
        empty_label=None,
        disabled=True
        )
    # done_by = SearchableModelField(
    #     queryset=CustomUser.objects.all(),
    #     search_url = search_users_url_path,
    #     all_url = all_users_url_path,
    #     repr_format = CustomUser_repr_format,
    #     model = CustomUser,
    #     choices = CustomUser.objects.all().only('user_id', 'first_name'),
    #     fk_field = 'user_id',
    #     disabled = True,
    #     required = False,
    #     empty_label = None # remove default option '------' from select menu
    #     )
    
    class Meta:
        model = SelfassesmentTracker
        fields = (
            # 'tracker_id',
            # 'created_by',
            # 'done_by',
            'client_id',
            'job_description',
            # 'complete_date',
            'is_completed',)

class SelfassesmentTrackerDeleteForm(forms.ModelForm):
    agree = forms.BooleanField(label='I want to proceed.', required=True)
    class Meta:
        model = Selfassesment
        fields = ()
