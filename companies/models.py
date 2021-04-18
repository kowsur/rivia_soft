from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .validators import BANK_ACCOUNT_NUMBER_VALIDATOR, SORT_CODE_VALIDATOR, UTR_VALIDATOR, NINO_VALIDATOR

# Create your models here.
class Selfassesment(models.Model):

    class Meta:
        verbose_name = _("Selfassesment")
        verbose_name_plural = _("Selfassesments")
    
    # identifies wheather the record is updated needs superuser permission
    is_updated = models.BooleanField(_('Update Status'), default=True, editable=False)

    created_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.PROTECT,
        verbose_name='Created by',
        related_name='utr_created_by',
        to_field='email',
        blank=True,
        null=True)
    client_id = models.AutoField(verbose_name='Unique ID for client', primary_key=True, unique=True, blank=True, null=False, editable=False, db_index=True) # auto incrementing primary field
    client_file_number = models.IntegerField(verbose_name='File Number', unique=True, blank=False, null=True, editable=True)
    client_name = models.CharField(verbose_name='Full Name', max_length=100, blank=False, null=False, db_index=True)
    client_phone_number = models.CharField(verbose_name='Phone numbers', max_length=255, blank=False, null=False, db_index=True)
    date_of_registration = models.DateField(verbose_name='Registration date', blank=False, null=False, default=timezone.now)
    UTR = models.CharField(
        verbose_name='UTR',
        max_length=10,
        blank=True,
        null=True,
        db_index=True,
        validators=[UTR_VALIDATOR])
    HMRC_referance = models.TextField(verbose_name='HMRC', max_length=2048, blank=True, null=True)
    NINO = models.CharField(
        verbose_name='NINO',
        max_length=9,
        blank=True,
        null=True,
        validators=[NINO_VALIDATOR])
    gateway_id = models.CharField(verbose_name='Gateway ID', max_length=255, blank=True, null=True)
    gateway_password = models.CharField(verbose_name='Gateway Password', max_length=255, blank=True, null=True)
    address = models.TextField(verbose_name='Address', blank=True, null=True, db_index=True)
    post_code = models.CharField(verbose_name='Postal Code', max_length=10, blank=True, null=True)
    email = models.EmailField(verbose_name='Email', max_length=320, blank=True, null=True)
    bank_name = models.CharField(verbose_name='Name of Bank', max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(
        verbose_name='Account number in Bank',
        max_length=8,
        blank=True,
        null=True,
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
    is_active = models.BooleanField(verbose_name='Active Status', blank=False, null=False, default=True)

    def __str__(self) -> str:
        return f'{self.client_id} - {self.client_name} - {self.client_phone_number}'
    
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
    client_id = models.ForeignKey(Selfassesment, on_delete=models.PROTECT, verbose_name='Client ID', to_field='client_id', blank=False, null=False)
    date_of_submission = models.DateField(verbose_name='Submission date', blank=True, null=True, default=timezone.now)
    tax_year = models.CharField(verbose_name='Tax Year', max_length=10, blank=True)
    submitted_by = models.ForeignKey(
        to='users.CustomUser', 
        on_delete=models.PROTECT,
        verbose_name='Submitted By', 
        related_name='submitted_by',
        to_field='user_id',
        blank=False,
        null=True)
    account_prepared_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.PROTECT,
        verbose_name='Prepared By',
        related_name='account_prepared_by',
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
        self.account_prepared_by = self.submitted_by
        self.save()
        


class Tracker(models.Model):

    class Meta:
        verbose_name = _("Tracker")
        verbose_name_plural = _("Trackers")

    tracker_id = models.AutoField(verbose_name = 'Tracker ID', blank=True, null=False, primary_key=True, db_index=True)
    creation_date = models.DateTimeField(verbose_name='Tracker creation datetime', editable=False, blank=True, null=False, default=timezone.now)
    created_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Created By',
        related_name='tracker_created_by',
        to_field='email',
        blank=False,
        null=False)
    done_by = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.RESTRICT,
        verbose_name='Done By',
        related_name='done_by',
        to_field='email',
        blank=True,
        null=True)
    client_id = models.ForeignKey(to=Selfassesment, on_delete=models.RESTRICT, verbose_name='Client ID', to_field='client_id', blank=False, null=False)
    job_description = models.TextField(verbose_name='Description', blank=True, null=True)
    deadline = models.DateField(verbose_name='Deadline', blank=False, null=False, default=timezone.now)
    complete_date = models.DateField(verbose_name='Complete Date', blank=True, null=True, default=timezone.now)
    is_completed = models.BooleanField(verbose_name='Status', blank=True, null=False, default=False)

    def __str__(self) -> str:
        if self.job_description:
            return f"{self.job_description}"
        return f"Deadline: {self.deadline} | Created By: {self.created_by}"
