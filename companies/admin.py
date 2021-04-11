from django.contrib import admin
from .models import Selfassesment, SelfassesmentAccountSubmission, Tracker


# Register your models here.
class TrackerAdmin(admin.ModelAdmin):
    # fields = ('created_by', 'done_by', 'client_id', 'job_description', 'deadline', 'complete_date', 'is_completed')
    model = Tracker
    list_display = ('created_by', 'done_by', 'client_id', 'job_description', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('job_description', 'created_by', 'done_by','deadline', 'complete_date')
    ordering = ('deadline', 'complete_date')

admin.site.register(Tracker, TrackerAdmin)


class SelfassesmentAdmin(admin.ModelAdmin):
  # fields = (
    # 'client_id',
    # 'client_file_number', 
    # 'client_name', 
    # 'client_phone_number', 
    # 'date_of_registration', 
    # 'UTR', 
    # 'HMRC_referance', 
    # 'NINO', 
    # 'gateway_id', 
    # 'gateway_password', 
    # 'address', 
    # 'post_code', 
    # 'email', 
    # 'bank_name', 
    # 'bank_account_number', 
    # 'bank_sort_code', 
    # 'bank_account_holder_name', 
    # 'is_active')
  model = Selfassesment
  list_display = ('client_name', 'date_of_registration', 'client_phone_number', 'email', 'is_active')
  list_filter = ('is_active',)
  search_fields = (
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
  ordering = ('date_of_registration',)
  fieldsets = (
        ('Client Info', {
            'classes': ('wide',),
            'fields': ('client_name', 'client_file_number', 'date_of_registration', 'is_active')
          }
        ),
        ('Contact Info', {
            'classes': ('wide',),
            'fields': ('client_phone_number', 'email', 'address', 'post_code')
          }
        ),
        ('Bank Info', {
            'classes': ('wide',),
            'fields': ('bank_account_holder_name', 'bank_name', 'bank_account_number', 'bank_sort_code')
          }
        ),
        (
          'Others', {
            'classes': ('wide',),
            'fields': ('UTR', 'HMRC_referance', 'NINO', 'gateway_id', 'gateway_password')
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
  #   'account_prepared_by', 
  #   'remarks', 
  #   'paid_amount', 
  #   'is_paid', 
  #   'is_submitted')
  model = SelfassesmentAccountSubmission
  list_display = ('client_id', 'remarks', 'paid_amount', 'is_paid', 'is_submitted')
  list_filter = ('is_paid', 'is_submitted')
  search_fields = ('is_updated',
    'submission_id',
    'client_id',
    'date_of_submission', 
    'tax_year', 
    'submitted_by', 
    'account_prepared_by', 
    'remarks', 
    'paid_amount', 
    'is_paid', 
    'is_submitted')
  ordering = ('tax_year', 'is_submitted', 'is_paid')
admin.site.register(SelfassesmentAccountSubmission, SelfassesmentAccountSubmissionAdmin)
