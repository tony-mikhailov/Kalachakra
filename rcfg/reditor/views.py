from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return HttpResponse(render(request, 'index.html', context={}), content_type='html; charset=utf-8')
    # if request.user.is_authenticated:
    #     else:
    #     return HttpResponseRedirect('/accounts/login')

