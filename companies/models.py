from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .validators import BANK_ACCOUNT_NUMBER_VALIDATOR, SORT_CODE_VALIDATOR, UTR_VALIDATOR, NINO_VALIDATOR


class SelfassesmentType(models.Model):
    
    class Meta:
        verbose_name = 'Selfassesment Type'
        verbose_name_plural = 'Selfassesment Types'
    
    type_id = models.AutoField(
        verbose_name='Selfassesment Type Id',
        primary_key=True,
        unique=True,
        editable=False,
        blank=True,
        null=False,
        db_index=True) # auto incrementing primary field
    type_name = models.CharField(
        verbose_name='Type Name',
        max_length=255,
        blank=False,
        null=False,
        default='New Selfassesment Type',
        db_index=True
        )
    
    def __str__(self) -> str:
        return f"{self.type_id} - {self.type_name}"
    


# Create your models here.
class Selfassesment(models.Model):

    class Meta:
        verbose_name = _("Selfassesment")
        verbose_name_plural = _("Selfassesments")
    
    # identifier
    client_id = models.AutoField(
        verbose_name='Unique ID for client',
        primary_key=True,
        unique=True,
        blank=True,
        null=False,
        editable=False,
        db_index=True) # auto incrementing primary field
    created_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.SET_NULL,
        verbose_name='Created by',
        related_name='selfassesment_created_by',
        to_field='user_id',
        blank=True,
        null=True)
    selfassesment_type = models.ForeignKey(
        to='companies.SelfassesmentType',
        on_delete=models.RESTRICT,
        verbose_name='Selfassesment Type',
        related_name='selfassesment_type_id',
        to_field='type_id',
        blank=False,
        null=True)
    date_of_registration = models.DateField(verbose_name='Registration date', blank=False, null=False, default=timezone.localtime)
    # identifies wheather the record is updated needs superuser permission
    is_updated = models.BooleanField(_('Update Status'), default=True, editable=False)
    is_active = models.BooleanField(verbose_name='Active Status', blank=False, null=False, default=True)
    remarks = models.TextField(_("Remarks"), blank=True, null=True)
    
    client_file_number = models.IntegerField(verbose_name='File Number', unique=True, blank=False, null=True, editable=True)
    client_name = models.CharField(verbose_name='Full Name / Business Name', max_length=100, blank=False, null=False, db_index=True)
    
    # Personal Info
    date_of_birth = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    PAYE_number = models.CharField(verbose_name='PAYE Number', max_length=255, blank=True, null=True, unique=True, db_index=True)
    personal_phone_number = models.CharField(verbose_name='Personal Phone numbers', max_length=255, blank=False, null=True, db_index=True)
    personal_email = models.EmailField(verbose_name='Personal Email', max_length=320, blank=True, null=True)
    personal_address = models.TextField(verbose_name='Personal Address', blank=True, null=True, db_index=True)
    personal_post_code =models.CharField(verbose_name='Personal Postal Code', max_length=10, blank=True, null=True)
    gateway_id = models.CharField(verbose_name='Personal Gateway ID', max_length=255, blank=True, null=True, unique=True)
    gateway_password = models.CharField(verbose_name='Gateway Password', max_length=255, blank=True, null=True)
    
    # Business Info
    AOR_number = models.CharField(verbose_name='Account Office Reference number', max_length=511, blank=True, null=True, db_index=True)
    business_phone_number = models.CharField(verbose_name='Business Phone numbers', max_length=255, blank=True, null=True, db_index=True)
    business_email = models.EmailField(verbose_name='Business Email', max_length=320, blank=True, null=True)
    business_address = models.TextField(verbose_name='Business Address', blank=True, null=True, db_index=True)
    business_post_code = models.CharField(verbose_name='Business Postal Code', max_length=10, blank=True, null=True)

    # HMRC Details
    HMRC_referance = models.CharField(verbose_name='HMRC Referance', max_length=1023, blank=True, null=True)
    UTR = models.CharField(
        verbose_name='UTR',
        max_length=10,
        blank=True,
        null=True,
        db_index=True,
        unique=True,
        validators=[UTR_VALIDATOR])
    NINO = models.CharField(
        verbose_name='NINO',
        max_length=9,
        blank=True,
        null=True,
        unique=True,
        validators=[NINO_VALIDATOR])
    HMRC_agent = models.BooleanField(verbose_name="HMRC agent active status", default=False, blank=False, null=False)
    
    # Bank Info
    bank_name = models.CharField(verbose_name='Name of Bank', max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(
        verbose_name='Account number in Bank',
        max_length=8,
        blank=True,
        null=True,
        # unique=True,
        validators=[BANK_ACCOUNT_NUMBER_VALIDATOR])
    bank_sort_code = models.CharField(
        verbose_name='Bank Sort Code',
        max_length=6,
        blank=True,
        null=True,
        validators=[SORT_CODE_VALIDATOR])
    bank_account_holder_name = models.CharField(
        verbose_name='Bank Account Holder Name',
        max_length=100,
        blank=True,
        null=False)

    def __str__(self) -> str:
        return f'👥{self.client_name} 📁{self.client_file_number} 📞{self.personal_phone_number} ☎{self.business_phone_number}'
    
    def __repr__(self) -> str:
        return str(self)

    # def save(self, *args, **kwargs):
    #     if not self.bank_account_holder_name:
    #         self.bank_account_holder_name = self.client_name
    #     if not type(self.client_file_number)==type(int):
    #         self.client_file_number = self.client_id
    #     super().save(*args, **kwargs)
    
    def set_defaults(self):
        if not isinstance(self.client_file_number, int):
            self.client_file_number = self.client_id
        if not self.bank_account_holder_name:
            self.bank_account_holder_name = self.client_name
        self.save()

    @classmethod
    def get_max_file_number(cls):
      try:
        max_num = cls.objects.all().order_by("-client_file_number")[0].client_file_number
        return max_num
      except IndexError:
        return 0
    
    @classmethod
    def get_next_file_number(cls):
      return cls.get_max_file_number()+1
    
    def approve_update_request(self):
        self.is_updated = True
        self.save()

    def request_to_update(self):
        self.is_updated=False
        self.save()


class SelfassesmentAccountSubmission(models.Model):

    class Meta:
        verbose_name = _("Selfassesment Submission")
        verbose_name_plural = _("Selfassesment Submissions")

    submission_id = models.AutoField(verbose_name='Submission ID', primary_key=True, null=False, db_index=True, editable=False)
    client_id = models.ForeignKey(
        to='companies.Selfassesment',
        on_delete=models.CASCADE,
        verbose_name='Client ID',
        to_field='client_id',
        related_name='selfassesment_account_submission_client_id',
        blank=False,
        null=False)
    date_of_submission = models.DateField(verbose_name='Submission date', blank=True, null=True, default=timezone.localtime)
    tax_year = models.CharField(verbose_name='Tax Year', max_length=10, blank=True)
    submitted_by = models.ForeignKey(
        to='users.CustomUser', 
        on_delete=models.CASCADE,
        verbose_name='Submitted By', 
        related_name='selfassesment_account_submission_submitted_by',
        to_field='user_id',
        blank=False,
        null=True)
    prepared_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name='Prepared By',
        related_name='selfassesment_account_submission_prepared_by',
        to_field='user_id',
        blank=True,
        null=True)
    remarks = models.TextField(verbose_name='Remarks', blank=True, null=True)
    paid_amount = models.BigIntegerField(verbose_name='Amount Paid', blank=True, null=True)
    is_paid = models.BooleanField(verbose_name='Is Paid', blank=True, null=False, default=False)
    is_submitted = models.BooleanField(verbose_name='Is Submitted', blank=True, null=False, default=False)

    def __str__(self):
        return f'Client: {self.client_id}, Submission Date: {self.date_of_submission}'
    
    def __repr__(self) -> str:
        return str(self)
    
    def set_defaults(self):
        self.prepared_by = self.submitted_by
        self.save()
        


class SelfassesmentTracker(models.Model):

    class Meta:
        verbose_name = _("Selfassesment Tracker")
        verbose_name_plural = _("Selfassesment Trackers")

    tracker_id = models.AutoField(verbose_name = 'Tracker ID', blank=True, null=False, primary_key=True, db_index=True)
    client_id = models.ForeignKey(
        to='companies.Selfassesment',
        on_delete=models.CASCADE,
        verbose_name='Client ID',
        to_field='client_id',
        related_name='selfassesment_tracker_client_id',
        blank=False,
        null=False)
    creation_date = models.DateTimeField(verbose_name='Creation Datetime', editable=False, blank=True, null=False, default=timezone.localtime)
    job_description = models.TextField(verbose_name='Description', blank=True, null=True)
    remarks = models.TextField(verbose_name="Remarks", blank=True, null=True, default='')
    has_issue = models.BooleanField(verbose_name="Has Issue", default=False)
    issue_created_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.SET_NULL,
        verbose_name='Issue Created By',
        related_name='selfassesment_tracker_issue_created_by',
        to_field='user_id',
        editable=False,
        blank=True,
        null=True
        )
    deadline = models.DateField(verbose_name='Deadline', blank=False, null=False, default=timezone.localtime)
    is_completed = models.BooleanField(verbose_name='Completed', blank=True, null=False, default=False)
    complete_date = models.DateField(verbose_name='Complete Date', blank=True, null=True)
    done_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.SET_NULL,
        verbose_name='Done By',
        related_name='selfassesment_tracker_done_by',
        to_field='user_id',
        blank=True,
        null=True)
    created_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Created By',
        related_name='selfassesment_tracker_created_by',
        to_field='user_id',
        blank=False,
        null=True)
    

    def __str__(self) -> str:
        if self.job_description:
            return f"{self.job_description}"
        return f"Deadline: {self.deadline} | Created By: {self.created_by}"



class Issue(models.Model):
    
    class Meta:
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'
    
    issue_id = models.AutoField(
        verbose_name='Issue Id',
        primary_key=True,
        unique=True,
        editable=False,
        blank=True,
        null=False,
        db_index=True) # auto incrementing primary field
    
    description = models.TextField(
        verbose_name='Type Name',
        max_length=255,
        blank=False,
        null=False,
        default='New Issue',
        db_index=True
        )
    
    def __str__(self) -> str:
        return f"{self.issue_id} - {self.description[:30]}"


class TrackerHasIssues(models.Model):
    tracker_id = models.ForeignKey(
        to='companies.SelfassesmentTracker',
        on_delete=models.CASCADE,
        verbose_name='Tracker Id',
        to_field='tracker_id',
        related_name='TrackerHasIssues_tracker_id',
        blank=False,
        null=False)
    issue_id = models.ForeignKey(
        to='companies.Issue',
        on_delete=models.PROTECT,
        verbose_name='Tracker Id',
        to_field='issue_id',
        related_name='TrackerHasIssues_issue_id',
        blank=False,
        null=False)
     