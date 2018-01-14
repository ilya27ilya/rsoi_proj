from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse

@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)