from django.contrib import admin
from .models import Selfassesment, SelfassesmentAccountSubmission, SelfassesmentTracker, SelfassesmentType
from .models import Limited, LimitedTracker, LimitedSubmissionDeadlineTracker, LimitedVATTracker, LimitedConfirmationStatementTracker


admin.site.register(SelfassesmentType)

# Register your models here.
class SelfassesmentTrackerAdmin(admin.ModelAdmin):
    # fields = ('created_by', 'done_by', 'client_id', 'job_description', 'deadline', 'complete_date', 'is_completed')
    model = SelfassesmentTracker
    list_display = ('created_by', 'done_by', 'client_id', 'job_description', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = (
      'tracker_id',
      'client_id__client_name',
      'client_id__client_file_number',
      'client_id__personal_email',
      'client_id__personal_phone_number',
      'client_id__personal_address',
      'client_id__personal_post_code',
      'client_id__business_email',
      'client_id__business_phone_number',
      'client_id__business_address',
      'client_id__business_post_code',
      'created_by__email', 
      'created_by__first_name', 
      'created_by__last_name', 
      'job_description',
      'created_by__email', 
      'created_by__first_name', 
      'created_by__last_name',
      'done_by__email', 
      'done_by__first_name', 
      'done_by__last_name', 
      'deadline',
      'complete_date')
    ordering = ('deadline', 'complete_date')

admin.site.register(SelfassesmentTracker, SelfassesmentTrackerAdmin)


class SelfassesmentAdmin(admin.ModelAdmin):
  # fields = (
    # 'client_id',
    # 'created_by', 
    # 'selfassesment_type',
    # 'date_of_registration',
    # 'is_updated',
    # 'is_active',
    # 'remarks',

    # 'client_file_number', 
    # 'client_name',

    # 'date_of_birth', 
    # 'PAYE_number', 
    # 'personal_phone_number', 
    # 'personal_email', 
    # 'personal_address', 
    # 'personal_post_code',

    # 'AOR_number',
    # 'business_phone_number',
    # 'business_email', 
    # 'business_address', 
    # 'business_post_code',

    # 'HMRC_agent', 
    # 'HMRC_referance', 
    # 'UTR', 
    # 'NINO', 
    # 'gateway_id', 
    # 'gateway_password', 
    
    # 'bank_name', 
    # 'bank_account_number', 
    # 'bank_sort_code', 
    # 'bank_account_holder_name',
    # )
  model = Selfassesment
  list_display = ('client_name', 'client_file_number', 'date_of_registration', 'business_phone_number', 'business_email', 'is_active')
  list_filter = ('is_active', 'date_of_registration')
  search_fields = (
    'client_id',
    'created_by__email', 
    'created_by__first_name', 
    'created_by__last_name', 
    'selfassesment_type__type_name',
    'date_of_registration',
    'is_updated',
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
  ordering = ('date_of_registration',)
  fieldsets = (
        # ('Identification', {
        #   'classes': ('wide', ),
        #   'fields': ('created_by', 'is_updated',)
        #   }
        # ),
        ('Client Info', {
            'classes': ('wide',),
            'fields': ('selfassesment_type', 'date_of_registration', 'remarks', 'is_active', 'client_file_number', 'client_name')
          }
        ),
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('date_of_birth', 'PAYE_number', 'personal_phone_number', 'personal_email', 'personal_address', 'personal_post_code', 'gateway_id', 'gateway_password', )
          }
        ),
        ('Business Info', {
            'classes': ('wide',),
            'fields': ('AOR_number', 'business_phone_number', 'business_email', 'business_address', 'business_post_code', )
          }
        ),
        ('Bank Info', {
            'classes': ('wide',),
            'fields': ('bank_name', 'bank_account_number', 'bank_sort_code', 'bank_account_holder_name',)
          }
        ),
        (
          'HMRC Details', {
            'classes': ('wide',),
            'fields': ('HMRC_referance', 'UTR', 'NINO', 'HMRC_agent', )
          }
        )
    )

admin.site.register(Selfassesment, SelfassesmentAdmin)


class SelfassesmentAccountSubmissionAdmin(admin.ModelAdmin):
  # fields = ('is_updated',
  #   'submission_id',
  #   'client_id',
  #   'date_of_submission', 
  #   'tax_year', 
  #   'submitted_by', 
  #   'prepared_by', 
  #   'remarks', 
  #   'paid_amount', 
  #   'is_paid', 
  #   'is_submitted')
  model = SelfassesmentAccountSubmission
  list_display = ('client_id', 'remarks', 'paid_amount', 'is_paid', 'is_submitted')
  list_filter = ('is_paid', 'is_submitted')
  search_fields = (
    'submission_id',
    'client_id__client_name',
    'client_id__client_file_number',
    'client_id__personal_email',
    'client_id__personal_phone_number',
    'client_id__personal_address',
    'client_id__personal_post_code',
    'client_id__business_email',
    'client_id__business_phone_number',
    'client_id__business_address',
    'client_id__business_post_code',
    'date_of_submission', 
    'tax_year', 
    'submitted_by__email', 
    'submitted_by__first_name', 
    'submitted_by__last_name',
    'prepared_by__email', 
    'prepared_by__first_name', 
    'prepared_by__last_name', 
    'remarks', 
    'paid_amount', 
    'is_paid', 
    'is_submitted')
  ordering = ('tax_year', 'is_submitted', 'is_paid')
admin.site.register(SelfassesmentAccountSubmission, SelfassesmentAccountSubmissionAdmin)


admin.site.register(Limited)
admin.site.register(LimitedTracker)
admin.site.register(LimitedSubmissionDeadlineTracker)
admin.site.register(LimitedVATTracker)
admin.site.register(LimitedConfirmationStatementTracker)
