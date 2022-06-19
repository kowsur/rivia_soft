import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from users.models import CustomUser
from .validators import BANK_ACCOUNT_NUMBER_VALIDATOR, SORT_CODE_VALIDATOR, UTR_VALIDATOR, NINO_VALIDATOR, AUTH_CODE_VALIDATOR, TAX_YEAR_VALIDATOR

from datetime import timedelta, date


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
    date_of_registration = models.DateField(verbose_name='Registration date', blank=False, null=False, default=timezone.now)
    # identifies wheather the record is updated needs superuser permission
    is_updated = models.BooleanField(_('Update Status'), default=True, editable=False)
    is_active = models.BooleanField(verbose_name='Active Status', blank=False, null=False, default=True)
    remarks = models.TextField(_("Remarks"), blank=True, null=True)
    
    client_file_number = models.DecimalField(verbose_name='File Number', max_digits=19, decimal_places=3, unique=True, blank=False, null=True, editable=True)
    client_name = models.CharField(verbose_name='Full Name / Business Name', max_length=100, blank=False, null=False, db_index=True)
    start_date = models.DateField(verbose_name='Selfassesment Start Date', blank=True, null=True, default=None)
    
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
        null=True)

    def __str__(self) -> str:
        return f'👥{self.client_name} 📁{self.client_file_number} 📞{self.personal_phone_number} 📭{self.personal_post_code}'
    
    def __repr__(self) -> str:
        return str(self)

    # def save(self, *args, **kwargs):
    #     if not self.bank_account_holder_name:
    #         self.bank_account_holder_name = self.client_name
    #     if not type(self.client_file_number)==type(int):
    #         self.client_file_number = self.client_id
    #     super().save(*args, **kwargs)
    
    def set_defaults(self):
        if not self.client_file_number:
            self.client_file_number = Selfassesment.get_next_file_number()
        
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

class SelfassesmentAccountSubmissionTaxYear(models.Model):
    class Meta:
        verbose_name = _("Selfassesment Tax Year")
        verbose_name_plural = _("Selfassesment Tax Years")
        constraints = [
            models.UniqueConstraint(fields=['tax_year'], name='unique_tax_year'),
        ]
    id = models.AutoField(verbose_name='Tax Year ID', primary_key=True, null=False, db_index=True, editable=False)
    tax_year = models.CharField(verbose_name='Tax Year', blank=False, null=False, max_length=12, validators=[TAX_YEAR_VALIDATOR])

    def __str__(self):
        return f"📆 {self.tax_year}"
    
    @classmethod
    def get_max_year(cls):
        years = cls.objects.all().order_by('-id')
        if years.count()>=1:
            return years.first()
        return None

class SelfassesmentAccountSubmission(models.Model):

    class Meta:
        verbose_name = _("Selfassesment Submission")
        verbose_name_plural = _("Selfassesment Submissions")
        constraints = [
            models.UniqueConstraint(
                fields = ('client_id', 'tax_year',),
                name = "unique_client_id__tax_year__status_SUBMITTED",
                )
        ]
        # unique_together = (
        #         ('client_id', 'tax_year',),
        #     )
    assigned_to = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Assigned to',
        related_name='selfassesment_account_submission_assigned_to',
        to_field='user_id',
        blank=True,
        null=True)
    submission_id = models.AutoField(verbose_name='Submission ID', primary_key=True, null=False, db_index=True, editable=False)
    client_id = models.ForeignKey(
        to='companies.Selfassesment',
        on_delete=models.CASCADE,
        verbose_name='Client ID',
        to_field='client_id',
        related_name='selfassesment_account_submission_client_id',
        blank=False,
        null=True)
    request_date = models.DateField("Request Date", blank=False, null=True, default=timezone.now)
    status_choices = (
        ("REQUEST", "REQUEST",),
        ("PRIORITY", "PRIORITY",),
        ("PROCESSING", "PROCESSING",),
        ("BOOK APPOINTMENT", "BOOK APPOINTMENT", ),
        ("READY FOR SUBMIT", "READY FOR SUBMIT", ),
        ("WAITING FOR INFORMATION", "WAITING FOR INFORMATION",),
        ("WAITING FOR CONFIRMATION", "WAITING FOR CONFIRMATION",),
        ("SUBMITTED", "SUBMITTED",)
    )
    status = models.CharField("Status", blank=False, max_length=55, choices=status_choices, default="REQUEST")
    appointment_date = models.DateField(verbose_name='Appointment Date', blank=True, null=True, default=timezone.now)
    tax_year = models.ForeignKey(
        default=SelfassesmentAccountSubmissionTaxYear.get_max_year,
        to=SelfassesmentAccountSubmissionTaxYear,
        on_delete=models.RESTRICT,
        to_field='id',
        null=True,
        blank=False)
    remarks = models.TextField(verbose_name='Comments', blank=True, null=True)
    submitted_by = models.ForeignKey(
        to='users.CustomUser', 
        on_delete=models.CASCADE,
        verbose_name='Submitted By', 
        related_name='selfassesment_account_submission_submitted_by',
        to_field='user_id',
        blank=False,
        null=True)
    is_submitted = models.BooleanField(verbose_name='Is Submitted', blank=True, null=False, default=False)
    is_data_collected = models.BooleanField(verbose_name='Is Data Collected', blank=True, null=False, default=False)
    prepared_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name='Prepared By',
        related_name='selfassesment_account_submission_prepared_by',
        to_field='user_id',
        blank=True,
        null=True)
    payment_status_choices = (
        ("NOT PAID", "NOT PAID"),
        ("PARTIALLY PAID", "PARTIALLY PAID"),
        ("PAID", "PAID"),
    )
    payment_status = models.CharField("Payment Status", blank=False, max_length=55, choices=payment_status_choices, default="NOT PAID")
    paid_amount = models.BigIntegerField(verbose_name='Amount Paid', blank=True, null=True)
    unique_public_view_key = models.UUIDField(default=uuid.uuid4, editable=False)

    last_updated_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Last Updated By',
        related_name='selfassesment_account_submission_last_updated_by',
        to_field='user_id',
        blank=False,
        null=True)
    last_updated_on = models.DateTimeField(verbose_name='Last Updated On', default=timezone.now, null=True)

    def __str__(self):
        return f'Client: {self.client_id}, Tax Year: {self.tax_year}'
    
    def __repr__(self) -> str:
        return str(self)
    
    def set_defaults(self, request):
        self.last_updated_by = request.user
        self.last_updated_on = timezone.now()
        
        if self.status == "SUBMITTED":
            self.is_submitted = True
            self.submitted_by = request.user
            self.date_of_submission = timezone.now()
        else:
            self.submitted_by = None
            self.is_submitted = False
            self.date_of_submission = None
        self.save()
    
    @classmethod
    def get_request_date(cls, client_id, tax_year):
        records = cls.objects.filter(client_id=client_id, tax_year=tax_year)
        if records.count()>=1:
            return records.first().request_date
        return None


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
        null=True)
    creation_date = models.DateTimeField(verbose_name='Creation Datetime', editable=False, blank=True, null=True, default=timezone.now)
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
    deadline = models.DateField(verbose_name='Deadline', blank=False, null=True, default=timezone.now)
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
    assigned_to = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Assigned to',
        related_name='selfassesment_tracker_assigned_to',
        to_field='user_id',
        blank=True,
        null=True)
    new_customer = models.BooleanField(verbose_name="New customer", blank=True, editable=False, default=False, null=True)

    def __str__(self) -> str:
        if self.job_description:
            return f"{self.job_description}"
        return f"Deadline: {self.deadline} | Created By: {self.created_by}"

class AutoCreatedSelfassesmentTracker(models.Model):
    class Meta:
        verbose_name = _("Auto Created Selfassesment Tracker")
        verbose_name_plural = _("Auto Created Selfassesment Trackers")
        constraints = [
                models.UniqueConstraint(
                    name = "Unique issue",
                    fields = ("selfassesment", "reference")
                    )
            ]
    selfassesment = models.ForeignKey(to='companies.Selfassesment', on_delete=models.CASCADE, to_field='client_id')
    selfassesment_tracker = models.ForeignKey(to='companies.SelfassesmentTracker', on_delete=models.CASCADE, to_field='tracker_id')
    
    class CreatedForField(models.TextChoices):
        NINO = "nino", _("NINO")
        UTR = "utr", _("UTR")
        HMRC_AGENT = "hmrc_agent", _("HMRC_AGENT")

    reference = models.CharField(max_length=15, choices=CreatedForField.choices)

    def __str__(self) -> str:
        return f"{self.selfassesment} - {self.reference}"



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
    id = models.AutoField(
        verbose_name='Issue Id',
        primary_key=True,
        unique=True,
        editable=False,
        blank=True,
        null=False,
        db_index=True) # auto id
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


#############################################################################################################
class Limited(models.Model):

    class Meta:
        verbose_name = _("Limited")
        verbose_name_plural = _("Limiteds")
    
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
        related_name='limited_created_by',
        to_field='user_id',
        blank=True,
        null=True)

    date_of_registration = models.DateField(verbose_name='Registration date', blank=False, null=True, default=timezone.now)
    is_active = models.BooleanField(verbose_name='Active Status', blank=False, null=False, default=True)
    remarks = models.TextField(_("Remarks"), blank=True, null=True)
    
    client_file_number = models.DecimalField(verbose_name='File Number', max_digits=19, decimal_places=3, unique=True, blank=False, null=True, editable=True)
    client_name = models.CharField(verbose_name='Business Name', max_length=100, blank=False, null=False, db_index=True)
    company_reg_number = models.CharField(verbose_name='Company Registration Number', max_length=100, blank=False, null=True, unique=True, db_index=True)
    company_auth_code = models.CharField(verbose_name='Company Authentication Code', max_length=100, blank=True, null=True, db_index=True, validators=[AUTH_CODE_VALIDATOR])
    
    # Director Info
    date_of_birth = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    PAYE_number = models.CharField(verbose_name='PAYE Number', max_length=255, blank=True, null=True, unique=True, db_index=True)
    director_name = models.CharField(verbose_name='Director Name', max_length=255, blank=True, null=True)
    director_phone_number = models.CharField(verbose_name='Director Phone numbers', max_length=255, blank=False, null=True, db_index=True)
    director_email = models.EmailField(verbose_name='Director Email', max_length=320, blank=True, null=True)
    director_address = models.TextField(verbose_name='Director Address', blank=True, null=True, db_index=True)
    director_post_code =models.CharField(verbose_name='Director Postal Code', max_length=10, blank=True, null=True)
    gateway_id = models.CharField(verbose_name='Director Gateway ID', max_length=255, blank=True, null=True, unique=True)
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
        null=True)
    
    vat = models.CharField(
        verbose_name='VAT',
        max_length=255,
        blank=True,
        null=True)

    def __str__(self) -> str:
        return f'🏢{self.client_name} 📂{self.client_file_number} ☎{self.director_phone_number} 📭{self.director_post_code} ⓇⓃ{self.company_reg_number}'
    
    def __repr__(self) -> str:
        return str(self)

    # def save(self, *args, **kwargs):
    #     if not self.bank_account_holder_name:
    #         self.bank_account_holder_name = self.client_name
    #     if not type(self.client_file_number)==type(int):
    #         self.client_file_number = self.client_id
    #     super().save(*args, **kwargs)
    
    def set_defaults(self):
        if not self.client_file_number:
            self.client_file_number = Limited.get_max_file_number()

        if not self.bank_account_holder_name:
            self.bank_account_holder_name = self.client_name
        self.save()

    @classmethod
    def get_max_file_number(cls):
      try:
        max_num = cls.objects.all().order_by("-client_file_number")[0].client_file_number
        max_num = int(max_num)
        return max_num
      except IndexError:
        return 0
    
    @classmethod
    def get_next_file_number(cls):
      return cls.get_max_file_number()+1


class LimitedTracker(models.Model):

    class Meta:
        verbose_name = _("Limited Tracker")
        verbose_name_plural = _("Limited Trackers")

    tracker_id = models.AutoField(verbose_name = 'Tracker ID', blank=True, null=False, primary_key=True, db_index=True)
    client_id = models.ForeignKey(
        to='companies.Limited',
        on_delete=models.CASCADE,
        verbose_name='Client ID',
        to_field='client_id',
        related_name='limited_tracker_client_id',
        blank=False,
        null=True)
    creation_date = models.DateTimeField(verbose_name='Creation Datetime', editable=False, blank=True, null=True, default=timezone.now)
    job_description = models.TextField(verbose_name='Description', blank=True, null=True)
    remarks = models.TextField(verbose_name="Remarks", blank=True, null=True, default='')
    has_issue = models.BooleanField(verbose_name="Has Issue", default=False)
    issue_created_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.SET_NULL,
        verbose_name='Issue Created By',
        related_name='limited_tracker_issue_created_by',
        to_field='user_id',
        editable=False,
        blank=True,
        null=True
        )
    deadline = models.DateField(verbose_name='Deadline', blank=False, null=True, default=timezone.now)
    is_completed = models.BooleanField(verbose_name='Completed', blank=True, null=False, default=False)
    complete_date = models.DateField(verbose_name='Complete Date', blank=True, null=True)
    done_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.SET_NULL,
        verbose_name='Done By',
        related_name='limited_tracker_done_by',
        to_field='user_id',
        blank=True,
        null=True)
    created_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Created By',
        related_name='limited_tracker_created_by',
        to_field='user_id',
        blank=False,
        null=True)
    assigned_to = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Assigned to',
        related_name='limited_tracker_assigned_to',
        to_field='user_id',
        blank=True,
        null=True)
    new_customer = models.BooleanField(verbose_name="New customer", blank=True, editable=False, default=False, null=True)

    def __str__(self) -> str:
        if self.job_description:
            return f"{self.job_description}"
        return f"Deadline: {self.deadline} | Created By: {self.created_by}"


class LimitedSubmissionDeadlineTracker(models.Model):
    class Meta:
        verbose_name = _("Limited Submission")
        verbose_name_plural = _("Limited Submissions")

    submission_id = models.AutoField(verbose_name='Submission ID', primary_key=True, null=False, db_index=True, editable=False)
    client_id = models.ForeignKey(
        to='companies.Limited',
        on_delete=models.CASCADE,
        verbose_name='Client ID',
        to_field='client_id',
        related_name='limited_account_submission_client_id',
        blank=False,
        null=True)
    
    status_choices = (
        ("DOCUMENT REQUESTED", "DOCUMENT REQUESTED"),
        ("WAITING FOR INFORMATION", "WAITING FOR INFORMATION"),
        ("DOCUMENT RECEIVED", "DOCUMENT RECEIVED"),
        ("PROCESSING", "PROCESSING"),
        ("WAITING FOR CONFIRMATION", "WAITING FOR CONFIRMATION"),
        ("COMPLETED", "COMPLETED"),
    )
    status = models.CharField("Status", blank=False, max_length=55, choices=status_choices, default="DOCUMENT REQUESTED")

    period_start_date = models.DateField(verbose_name='Period Start', blank=True, null=True)
    period = models.DateField(
        verbose_name='Period End',
        blank=True,
        null=True,
        db_index=False
    )
    
    our_deadline = models.DateField(verbose_name='HMRC Deadline', blank=True, null=True)
    is_submitted_hmrc = models.BooleanField(verbose_name='Is Submitted(HM)', default=False, null=False)
    submitted_by_hmrc = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Submitted By(HM)',
        related_name='limited_submission_submitted_by_hmrc',
        to_field='user_id',
        blank=True,
        null=True)
    submission_date_hmrc = models.DateField(verbose_name='Submission Date(HM)', blank=True, null=True)

    HMRC_deadline = models.DateField(verbose_name='CompanyHouse Deadline', blank=False, null=True)
    is_submitted = models.BooleanField(verbose_name='Is Submitted(CH)', default=False, null=False)
    submitted_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Submitted By(CH)',
        related_name='limited_submission_submitted_by',
        to_field='user_id',
        blank=True,
        null=True)
    submission_date = models.DateField(verbose_name='Submission Date(CH)', blank=True, null=True)
    is_documents_uploaded = models.BooleanField(verbose_name='Is Documents Uploaded', default=False, null=False)
    remarks = models.TextField(verbose_name='Remarks', blank=True, null=True)
    updated_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Last Updated By',
        related_name='limited_submission_updated_by',
        to_field='user_id',
        blank=False,
        null=True)
    last_updated_on = models.DateTimeField(verbose_name='Last Updated On', null=True, auto_now=True)


    def __str__(self) -> str:
        return f"{self.submission_id} - {self.client_id}"


    def set_defaults(self, request):
        self.updated_by = request.user
        self.last_updated_on = timezone.now()
        if not type(self.HMRC_deadline) == type(date(2021, 6, 28)):
            raise ValueError("HMRC_deadline should be an instance of datetime.date")
        
        # set self.our_deadline 30 days before the self.HMRC_deadline
        self.our_deadline = self.HMRC_deadline + timedelta(45)
        self.save()

# Limited VAT Tracker
class LimitedVATTracker(models.Model):
    class Meta:
        verbose_name = _("Limited VAT Tracker")
        verbose_name_plural = _("Limited VAT Trackers")

    vat_id = models.AutoField(verbose_name='VAT Tracker ID', primary_key=True, null=False, db_index=True, editable=False)
    client_id = models.ForeignKey(
        to='companies.Limited',
        on_delete=models.CASCADE,
        verbose_name='Client ID',
        to_field='client_id',
        related_name='limited_vat_client_id',
        blank=False,
        null=True)
    period_start = models.DateField(verbose_name='Period Start', blank=False, null=True)
    period_end = models.DateField(verbose_name='Period End', blank=False, null=True)
    HMRC_deadline = models.DateField(verbose_name='HMRC Deadline', blank=True, null=True)
    is_submitted = models.BooleanField(verbose_name='Is Submitted', default=False, null=False)
    submitted_by = models.TextField(verbose_name='Submitted By', blank=True, default='', null=True)
    submission_date = models.DateField(verbose_name='Submission Date', blank=True, null=True)
    is_documents_uploaded = models.BooleanField(verbose_name='Is Documents Uploaded', default=False, null=False)
    remarks = models.TextField(verbose_name='Remarks', blank=True, null=True)
    updated_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Last Updated By',
        related_name='limited_vat_updated_by',
        to_field='user_id',
        blank=False,
        null=True)
    last_updated_on = models.DateTimeField(verbose_name='Last Updated On', default=timezone.now, null=True)

    def __str__(self) -> str:
        return f"{self.vat_id} - {self.client_id}"

    def set_defaults(self, request):
        self.updated_by = request.user
        self.last_updated_on = timezone.now()
        
        if self.period_end:
            # set self.our_deadline 30 days before the self.HMRC_deadline
            self.HMRC_deadline = self.period_end + timedelta(30)
        self.save()


# Limited Confirmation Statement Tracker
class LimitedConfirmationStatementTracker(models.Model):
    class Meta:
        verbose_name = _("Limited Confirmation Statement")
        verbose_name_plural = _("Limited Confirmation Statements")

    statement_id = models.AutoField(verbose_name='Statement ID', primary_key=True, null=False, db_index=True, editable=False)
    client_id = models.ForeignKey(
        to='companies.Limited',
        on_delete=models.CASCADE,
        verbose_name='Client ID',
        to_field='client_id',
        related_name='limited_confirmation_client_id',
        blank=False,
        null=True)
    HMRC_deadline = models.DateField(verbose_name='HMRC Deadline', blank=False, null=True)
    is_submitted = models.BooleanField(verbose_name='Is Submitted', default=False, null=False)
    submitted_by = models.TextField(verbose_name='Submitted By', blank=True, default='', null=True)
    submission_date = models.DateField(verbose_name='Submission Date', blank=True, null=True)
    is_documents_uploaded = models.BooleanField(verbose_name='Is Documents Uploaded', default=False, null=False)
    remarks = models.TextField(verbose_name='Remarks', blank=True, null=True)
    updated_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Last Updated By',
        related_name='limited_confirmation_updated_by',
        to_field='user_id',
        blank=False,
        null=True)
    last_updated_on = models.DateTimeField(verbose_name='Last Updated On', default=timezone.now, null=True)


    def __str__(self) -> str:
        return f"{self.statement_id} - {self.client_id}"


    def set_defaults(self, request):
        self.updated_by = request.user
        self.last_updated_on = timezone.now()
        self.save()


class SelfemploymentIncomeAndExpensesDataCollection(models.Model):
    class Model:
        verbose_name = 'Selfemployment Class 2 Tax Config For TaxYear'
        verbose_name_plural = 'Selfemployment Class 2 Tax Configs For TaxYears'
        constraints = [
            models.UniqueConstraint(
                fields = ('selfassesment', 'tax_year'),
                name = "SelfemploymentIncomeAndExpensesDataCollection__selfassesment__tax_year",
                )
        ]

    selfassesment = models.ForeignKey(Selfassesment, on_delete=models.CASCADE)
    tax_year = models.ForeignKey(SelfassesmentAccountSubmissionTaxYear, on_delete=models.RESTRICT, default=SelfassesmentAccountSubmissionTaxYear.get_max_year)

    # incomes
    uber_income = models.FloatField(_('Uber'), default=0, validators=[MinValueValidator(0)])
    bolt_income = models.FloatField(_('Bolt'), default=0, validators=[MinValueValidator(0)])
    free_now_income = models.FloatField(_('Free now'), default=0, validators=[MinValueValidator(0)])
    other_income = models.FloatField(_('Others'), default=0, validators=[MinValueValidator(0)])
    total_grant_income = models.FloatField(_('Total grant(last two) received'), default=0, validators=[MinValueValidator(0)])
    employment_income = models.FloatField(_('Employment Income(Please send P60 or P45)'), default=0, validators=[MinValueValidator(0)])
    income_note = models.TextField(_("Note: (Please write below where did you send documents? Email/WhatsApp)"))

    # expenses
    telephone_expense = models.FloatField(_('Telephone'), default=0, validators=[MinValueValidator(0)])
    congestion_expense = models.FloatField(_('Congestion Charge'), default=0, validators=[MinValueValidator(0)])
    insurance_expense = models.FloatField(_('Insurance'), default=0, validators=[MinValueValidator(0)])
    MOT_expense = models.FloatField(_('MOT'), default=0, validators=[MinValueValidator(0)])
    licence_expense = models.FloatField(_('Licence Renew'), default=0, validators=[MinValueValidator(0)])
    repair_expense = models.FloatField(_('Repair'), default=0, validators=[MinValueValidator(0)])
    road_tax_expense = models.FloatField(_('Road Tax'), default=0, validators=[MinValueValidator(0)])
    breakdown_expense = models.FloatField(_('Breakdown'), default=0, validators=[MinValueValidator(0)])
    car_value_expense = models.FloatField(_('Car Value'), default=0, validators=[MinValueValidator(0)])

    is_submitted = models.BooleanField(_("Ready to Submit"), default=False)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)


    def __str__(self):
        return f"{self.tax_year} - {self.selfassesment}"


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=SelfemploymentIncomeAndExpensesDataCollection, weak=False)
def update_selfassesment_account_submission_Is_Data_Collected(sender, instance, created, **kwargs):
    selfassesment = instance.selfassesment
    tax_year = instance.tax_year

    account_submission = SelfassesmentAccountSubmission.objects.filter(client_id=selfassesment, tax_year=tax_year).first()
    if account_submission:
        account_submission.is_data_collected = True
        account_submission.save()

@receiver(pre_save, sender=SelfassesmentAccountSubmission, weak=False)
def set_selfassesment_account_submission_Is_Data_Collected_field_value(sender, instance, **kwargs):
    selfassesment = instance.client_id
    tax_year = instance.tax_year

    data_collection = SelfemploymentIncomeAndExpensesDataCollection.objects.filter(selfassesment=selfassesment, tax_year=tax_year).first()
    if data_collection:
        instance.is_data_collected = True
