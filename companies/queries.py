from django.db.models import Q
from .models import Selfassesment, SelfassesmentAccountSubmission, SelfassesmentTracker
from .models import Limited

# =============================================================================================================
# =============================================================================================================
# Selfassesment
def db_search_Selfassesment(search_text: str, limit=-1):
    Query = Q(selfassesment_type__type_name__icontains = search_text) |\
            Q(date_of_registration__icontains          = search_text) |\
            Q(remarks__icontains                       = search_text) |\
            Q(client_name__icontains                   = search_text) |\
            Q(date_of_birth__icontains                 = search_text) |\
            Q(PAYE_number__icontains                   = search_text) |\
            Q(personal_phone_number__icontains         = search_text) |\
            Q(personal_email__icontains                = search_text) |\
            Q(personal_address__icontains              = search_text) |\
            Q(personal_post_code__icontains            = search_text) |\
            Q(AOR_number__icontains                    = search_text) |\
            Q(business_phone_number__icontains         = search_text) |\
            Q(business_email__icontains                = search_text) |\
            Q(business_address__icontains              = search_text) |\
            Q(business_post_code__icontains            = search_text) |\
            Q(HMRC_agent__icontains                    = search_text) |\
            Q(HMRC_referance__icontains                = search_text) |\
            Q(UTR__icontains                           = search_text) |\
            Q(NINO__icontains                          = search_text) |\
            Q(gateway_id__icontains                    = search_text) |\
            Q(gateway_password__icontains              = search_text) |\
            Q(bank_name__icontains                     = search_text) |\
            Q(bank_account_number__icontains           = search_text) |\
            Q(bank_sort_code__icontains                = search_text) |\
            Q(bank_account_holder_name__icontains      = search_text)

    try:
        num = int(search_text)
        Query |= Q(client_id          = num) |\
                 Q(client_file_number = num)
    except Exception:
        pass
    
    if limit==-1:
        return Selfassesment.objects.filter(Query)
    return Selfassesment.objects.filter(Query)[:limit]

def db_all_Selfassesment(limit=-1):
    if limit<=-1:
        return Selfassesment.objects.all()
    return Selfassesment.objects.all()[:limit]

# SelfassesmentAccountSubmission
def db_search_SelfassesmentAccountSubmission(search_text: str, limit=-1):
    Query = Q(date_of_submission__icontains               = search_text) |\
            Q(tax_year__icontains                         = search_text) |\
            Q(client_id__client_name__icontains           = search_text) |\
            Q(client_id__personal_phone_number__icontains = search_text) |\
            Q(client_id__business_phone_number__icontains = search_text) |\
            Q(submitted_by__email__icontains              = search_text) |\
            Q(submitted_by__first_name__icontains         = search_text) |\
            Q(submitted_by__last_name__icontains          = search_text) |\
            Q(prepared_by__email__icontains               = search_text) |\
            Q(prepared_by__first_name__icontains          = search_text) |\
            Q(prepared_by__last_name__icontains           = search_text) |\
            Q(remarks__icontains                          = search_text)
    try:
        num = int(search_text)
        Query |= Q(submission_id                = num) |\
                Q(client_id__client_file_number = num) |\
                Q(client_id                     = num) |\
                Q(paid_amount                   = num)
    except Exception:
        pass
    
    if limit==-1:
        return SelfassesmentAccountSubmission.objects.filter(Query)
    return SelfassesmentAccountSubmission.objects.filter(Query)[:limit]


def db_all_SelfassesmentAccountSubmission(limit=-1):
    if limit<=-1:
        return SelfassesmentAccountSubmission.objects.all()
    return SelfassesmentAccountSubmission.objects.all()[:limit]


# =============================================================================================================
# =============================================================================================================
# SelfassesmentTracker
def db_search_SelfassesmentTracker(search_text: str, user_email='', is_superuser=False, limit=-1):
    Query = Q(job_description__icontains                  = search_text) |\
            Q(deadline__icontains                         = search_text) |\
            Q(client_id__client_name__icontains           = search_text) |\
            Q(client_id__personal_phone_number__icontains = search_text) |\
            Q(client_id__business_phone_number__icontains = search_text) |\
            Q(client_id__client_file_number__icontains    = search_text) |\
            Q(created_by__first_name__icontains           = search_text) |\
            Q(created_by__last_name__icontains            = search_text) |\
            Q(done_by__first_name__icontains              = search_text) |\
            Q(done_by__last_name__icontains               = search_text)
    
    # # created by should be the current logged in user
    # if not is_superuser:
    #     Query &= Q(created_by__email = user_email)
    
    # Filter records from db using query
    if limit==-1:
        records = SelfassesmentTracker.objects.filter(Query)
    else:
        records = SelfassesmentTracker.objects.filter(Query)[:limit]
    return records.order_by('is_completed', '-pk')

def db_all_SelfassesmentTracker(user_email='', is_superuser=False, limit=-1):
    Query = Q()
    # # created by should be the current logged in user
    # if not is_superuser:
    #     Query = Query & Q(created_by__email = user_email)
    
    if limit==-1:
        records = SelfassesmentTracker.objects.filter(Query)
    else:
        records = SelfassesmentTracker.objects.filter(Query)[:limit]
    return records.order_by('is_completed', '-pk')



# =============================================================================================================
# =============================================================================================================
# Limited
def db_search_Limited(search_text: str, limit=-1):
    Query = Q(date_of_registration__icontains          = search_text) |\
            Q(remarks__icontains                       = search_text) |\
            Q(client_name__icontains                   = search_text) |\
            Q(company_reg_number__icontains            = search_text) |\
            Q(company_auth_code__icontains             = search_text) |\
            Q(date_of_birth__icontains                 = search_text) |\
            Q(PAYE_number__icontains                   = search_text) |\
            Q(director_phone_number__icontains         = search_text) |\
            Q(director_email__icontains                = search_text) |\
            Q(director_address__icontains              = search_text) |\
            Q(director_post_code__icontains            = search_text) |\
            Q(AOR_number__icontains                    = search_text) |\
            Q(business_phone_number__icontains         = search_text) |\
            Q(business_email__icontains                = search_text) |\
            Q(business_address__icontains              = search_text) |\
            Q(business_post_code__icontains            = search_text) |\
            Q(HMRC_agent__icontains                    = search_text) |\
            Q(HMRC_referance__icontains                = search_text) |\
            Q(UTR__icontains                           = search_text) |\
            Q(NINO__icontains                          = search_text) |\
            Q(gateway_id__icontains                    = search_text) |\
            Q(gateway_password__icontains              = search_text) |\
            Q(bank_name__icontains                     = search_text) |\
            Q(bank_account_number__icontains           = search_text) |\
            Q(bank_sort_code__icontains                = search_text) |\
            Q(bank_account_holder_name__icontains      = search_text)

    try:
        num = float(search_text)
        Query |= Q(client_id          = num) |\
                 Q(client_file_number = num)
    except Exception:
        pass
    
    if limit==-1:
        return Limited.objects.filter(Query)
    return Limited.objects.filter(Query)[:limit]

def db_all_Limited(limit=-1):
    if limit<=-1:
        return Limited.objects.all()
    return Limited.objects.all()[:limit]
