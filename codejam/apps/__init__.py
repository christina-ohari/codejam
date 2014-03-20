# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import render
from codejam.apps.contest.models import Contest


def index(request):
  variables = {'is_opened': True}
  try:
    c = Contest.objects.get(visible=True, expired_at__gte=datetime.now())
    variables.update({'id': c.id, 'title': c.title, 'opened_at': c.opened_at.strftime('%b %d %Y %H:%M:%S UTC')})
  except Contest.DoesNotExist:
    variables['is_opened'] = False
  return render(request, '2014_home.html', variables)


def participate(request):
  if request.user.is_authenticated():
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect('/codejam')
  return render(request, 'index.html')


def schedule(request):
  return render(request, '2014_schedule.html')


def terms(request):
  return render(request, '2014_terms.html')