from .models import CustomUser
from django.db.models import Q

def search_CustomUser_by_email(search_text:str, limit:int = -1):
    if limit<-1:
        raise ValueError("Limit can't be smaller than -1")
    
    Query = Q(email__icontains = search_text)

    results = CustomUser.objects.filter(Query).only('user_id')
    if limit==-1:
        return results
    return results[:limit]


def search_CustomUser(search_text:str, limit:int = -1):
    if limit<-1:
        raise ValueError("Limit can't be smaller than -1")
    
    Query = Q(email__icontains       = search_text)|\
            Q(first_name__icontains  = search_text)|\
            Q(last_name__icontains   = search_text)
    
    results = CustomUser.objects.filter(Query).only('user_id')
    if limit==-1:
        return results
    return results[:limit]
