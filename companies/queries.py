from django.db.models import Q
from .models import Selfassesment, SelfassesmentAccountSubmission, SelfassesmentTracker


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
            Q(submitted_by__email__contains         = search_text) |\
            Q(account_prepared_by__email__contains  = search_text) |\
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
    Query = Q(done_by__email__contains      = search_text) |\
            Q(job_description__contains     = search_text) |\
            Q(deadline__contains            = search_text) |\
            Q(complete_date__contains       = search_text) |\
            Q(is_completed__contains        = search_text)
    
    if search_text.isnumeric():
        Query = Query | Q(tracker_id        = search_text) |\
                        Q(client_id         = search_text)
    # created by should be the current logged in user
    Query = Query & Q(created_by__email = user)
    
    if limit==-1:
        return SelfassesmentTracker.objects.filter(Query)
    return SelfassesmentTracker.objects.filter(Query)[:limit]

def db_all_SelfassesmentTrackers(limit=-1):
    if limit<=-1:
        return SelfassesmentTracker.objects.all()
    return SelfassesmentTracker.objects.all()[:limit]
