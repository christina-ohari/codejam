# -*- coding: utf-8 -*-
import re
from datetime import datetime
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from codejam.apps.contest.models import Contest



@require_POST
@login_required
def create(request):

  if not request.user.is_staff:
    raise Http404
  
  post = request.POST.copy()

  p = re.compile('^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2}) (?P<hour>\d{1,2}):(?P<min>\d{1,2})$')

  m = p.match(post['contest_opened'])
  if m == None:
    r = HttpResponse('opened date format is invalid.', content_type='text/plain')
    # find correct status code
    r.status_code = 403
    return r
  
  opened = datetime(int(m.group('year'))
                    , int(m.group('month'))
                    , int(m.group('day'))
                    , int(m.group('hour'))
                    , int(m.group('min')))
  
  m = p.match(post['contest_expired'])
  if m == None:
    r = HttpResponse('expired date format is invalid.', content_type='text/plain')
    # find correct status code
    r.status_code = 403
    return r
  
  expired = datetime(int(m.group('year'))
                     , int(m.group('month'))
                     , int(m.group('day'))
                     , int(m.group('hour'))
                     , int(m.group('min')))
  
  if not opened < expired:
    r = HttpResponse('expired date shoul greater than opend date.', content_type='text/plain')
    # find correct status code
    r.status_code = 403
    return r

  q1 = Q(opened_at__lte=opened) & Q(expired_at__gte=opened)
  q2 = Q(opened_at__lte=expired) & Q(expired_at__gte=expired)
  if Contest.objects.filter(q1 | q2).exists():
    r = HttpResponse('there is another contest between opened and closed date.', content_type='text/plain')
    # find correct status code
    r.status_code = 403
    return r

  title = post['contest_title']
  # check title validation
  print title
  
  Contest.objects.create(title=title, opened_at=opened, expired_at=expired)

  contests = Contest.objects.all().values()
  return render(request, 'contest/list.html', {contests: contests})
