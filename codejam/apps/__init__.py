# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
    if request.user.is_authenticated():
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect('/codejam/contest/0/dashboard')
    variables = RequestContext(request, {})
    return render_to_response('index.html', variables)
