# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render


def index(request):
  if request.user.is_authenticated():
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect('/codejam/dashboard')
  return render(request, 'index.html')



def schedule(request):
    return render(request, '2014_schedule.html')



def terms(request):
    return render(request, '2014_terms.html')