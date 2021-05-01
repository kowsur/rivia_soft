from django.db.models import Q
from .models import Selfassesment, SelfassesmentAccountSubmission, SelfassesmentTracker
from .models import Limited, LimitedAccountSubmission, LimitedTracker

# =============================================================================================================
# =============================================================================================================
# Selfassesment
def db_search_Selfassesment(search_text: str, limit=-1):
    Query = Q(client_name__contains             = search_text) |\
            Q(client_file_number__contains      = search_text) |\
            Q(client_phone_number__contains     = search_text) |\
            Q(date_of_registration__contains    = search_text) |\
            Q(HMRC_referance__contains          = search_text) |\
            Q(gateway_id__contains              = search_text) |\
            Q(gateway_password__contains        = search_text) |\
            Q(address__contains                 = search_text) |\
            Q(post_code__contains               = search_text) |\
            Q(email__contains                   = search_text) |\
            Q(bank_name__contains               = search_text) |\
            Q(bank_account_number__contains     = search_text) |\
            Q(bank_sort_code__contains          = search_text) |\
            Q(bank_account_holder_name__contains= search_text) |\
            Q(UTR                               = search_text) |\
            Q(NINO                              = search_text)
    if search_text.isnumeric():
        Query = Query | Q(client_id                    = int(search_text))
    
    if limit==-1:
        return Selfassesment.objects.filter(Query)
    return Selfassesment.objects.filter(Query)[:limit]

def db_all_Selfassesment(limit=-1):
    if limit<=-1:
        return Selfassesment.objects.all()
    return Selfassesment.objects.all()[:limit]

# SelfassesmentAccountSubmission
def db_search_SelfassesmentAccountSubmission(search_text: str, limit=-1):
    Query = Q(date_of_submission__contains          = search_text) |\
            Q(tax_year__contains                    = search_text) |\
            Q(client_id__client_name__contains = search_text) |\
            Q(client_id__client_phone_number__contains = search_text) |\
            Q(client_id__client_file_number__contains = search_text) |\
            Q(submitted_by__email__contains         = search_text) |\
            Q(prepared_by__email__contains          = search_text) |\
            Q(remarks__contains                     = search_text)

    if search_text.isnumeric():
        Query = Query | Q(submission_id             = search_text) |\
                        Q(client_id                 = search_text) |\
                        Q(paid_amount               = search_text)
    
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
def db_search_SelfassesmentTracker(search_text: str, user='admin@gmail.com', limit=-1):
    Query = Q(job_description__contains     = search_text) |\
            Q(deadline__contains            = search_text) |\
            Q(client_id__client_name__contains = search_text) |\
            Q(client_id__client_phone_number__contains = search_text) |\
            Q(client_id__client_file_number__contains = search_text)
            # Q(created_by__first_name__contains = search_text) |\
            # Q(created_by__last_name__contains = search_text) |\
            # Q(done_by__first_name__contains = search_text) |\
            # Q(done_by__last_name__contains = search_text)
    
    # created by should be the current logged in user
    # Query = Query & Q(created_by__email = user)
    
    # Filter records from db using query
    if limit==-1:
        records = SelfassesmentTracker.objects.filter(Query)
    else:
        records = SelfassesmentTracker.objects.filter(Query)[:limit]
    return records.order_by('is_completed', 'deadline')

def db_all_SelfassesmentTracker(limit=-1):
    if limit==-1:
        records = SelfassesmentTracker.objects.all()
    else:
        records = SelfassesmentTracker.objects.all()[:limit]
    return records.order_by('is_completed', 'deadline')



# =============================================================================================================
# =============================================================================================================
# Limited
def db_search_Limited(search_text: str, limit=-1):
    Query = Q(client_name__contains             = search_text) |\
            Q(client_file_number__contains      = search_text) |\
            Q(client_phone_number__contains     = search_text) |\
            Q(date_of_registration__contains    = search_text) |\
            Q(HMRC_referance__contains          = search_text) |\
            Q(gateway_id__contains              = search_text) |\
            Q(gateway_password__contains        = search_text) |\
            Q(address__contains                 = search_text) |\
            Q(post_code__contains               = search_text) |\
            Q(email__contains                   = search_text) |\
            Q(bank_name__contains               = search_text) |\
            Q(bank_account_number__contains     = search_text) |\
            Q(bank_sort_code__contains          = search_text) |\
            Q(bank_account_holder_name__contains= search_text) |\
            Q(UTR                               = search_text) |\
            Q(NINO                              = search_text)
    if search_text.isnumeric():
        Query = Query | Q(client_id                    = int(search_text))
    
    if limit==-1:
        return Limited.objects.filter(Query)
    return Limited.objects.filter(Query)[:limit]

def db_all_Limited(limit=-1):
    if limit<=-1:
        return Limited.objects.all()
    return Limited.objects.all()[:limit]

# LimitedAccountSubmission
def db_search_LimitedAccountSubmission(search_text: str, limit=-1):
    Query = Q(date_of_submission__contains          = search_text) |\
            Q(tax_year__contains                    = search_text) |\
            Q(submitted_by__email__contains         = search_text) |\
            Q(account_prepared_by__email__contains  = search_text) |\
            Q(remarks__contains                     = search_text)

    if search_text.isnumeric():
        Query = Query | Q(submission_id             = search_text) |\
                        Q(client_id                 = search_text) |\
                        Q(paid_amount               = search_text)
    
    if limit==-1:
        return LimitedAccountSubmission.objects.filter(Query)
    return LimitedAccountSubmission.objects.filter(Query)[:limit]


def db_all_LimitedAccountSubmission(limit=-1):
    if limit<=-1:
        return LimitedAccountSubmission.objects.all()
    return LimitedAccountSubmission.objects.all()[:limit]


# =============================================================================================================
# =============================================================================================================
# LimitedTracker
def db_search_LimitedTracker(search_text: str, user='admin@gmail.com', limit=-1):
    Query = Q(done_by__email__contains      = search_text) |\
            Q(job_description__contains     = search_text) |\
            Q(deadline__contains            = search_text) |\
            Q(complete_date__contains       = search_text) |\
            Q(is_completed__contains        = search_text)
    
    if search_text.isnumeric():
        Query = Query | Q(tracker_id        = search_text) |\
                        Q(client_id         = search_text)
    # created by should be the current logged in user
    # Query = Query & Q(created_by__email = user)
    
    # filter records using the query
    if limit==-1:
        return LimitedTracker.objects.filter(Query).order_by('-deadline')
    return LimitedTracker.objects.filter(Query)[:limit]

def db_all_LimitedTracker(limit=-1):
    if limit<=-1:
        return LimitedTracker.objects.all().order_by('-deadline')
    return LimitedTracker.objects.all()[:limit]
