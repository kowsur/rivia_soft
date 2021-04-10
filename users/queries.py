from .models import CustomUser
from django.db.models import Q

def CustomUser_search_by_email(search_text:str, limit:int = -1):
    if limit<-1:
        raise ValueError("Limit can't be smaller than -1")
    Query = Q(email__contains = search_text)
    results = CustomUser.objects.filter(Query).only(fields=('email'))
    if limit==-1:
        return results
    return results[:limit]
