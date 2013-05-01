# -*- coding: utf-8 -*-
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from codejam.apps.contest.models import Answer
from codejam.apps.problem.models import Problem
from codejam.apps.problem.models import IO

def dashboard(request, id):
    result = {}
    get = request.GET.copy()

    problems = Problem.objects.all().values();
    
    menu = []
    if len(problems) > 0:
        index = 0
        if get.has_key('p'):
            index = int(get['p'])
        p = problems[index]
        result['index'] = index
        result['problem'] = p
        
        inputs = IO.objects.filter(problem__id=p['id']).values()
        if len(inputs) > 0:
            import random
            result['io'] = inputs[random.randrange(len(inputs))]['id']

        deco = ord('A')
        for p in problems:
            info = {'id': p['id'], 'deco': chr(deco), 'name': p['name']}
            menu.append(info)
            if result['problem']['id'] == p['id']:
                result['problem']['deco'] = chr(deco)
            deco = deco + 1
    result['menu'] = menu

    variables = RequestContext(request, result)
    return render_to_response('contest/dashboard.html', variables)



@require_POST
@login_required
def dashboard_do(request, id):
    post = request.POST.copy()
    files = request.FILES.copy()
    
    cmd = post.get('cmd', False)
    if not cmd or cmd != 'SubmitAnswer':
        # return HttpResponseBadRequest()
        raise Http404
    id = post.get('problem', False)
    if not id:
        # return HttpResponseBadRequest()
        raise Http404
    input = post.get('input_id', False)
    if not input:
        # return HttpResponseBadRequest()
        raise Http404
    
    answer = files.get('answer', False)
    if not answer:
        # return HttpResponseBadRequest()
        raise Http404
    source = files.get('source', False)
    if not source:
        # return HttpResponseBadRequest()
        raise Http404
        

    try:
        io = IO.objects.get(id=input, problem__id=id)

        data_output = ''
        for chunk in answer.chunks():
            data_output += chunk

        data_source = ''
        for chunk in answer.chunks():
            data_source += chunk
        
        points = 0
        problem = Problem.objects.get(id=id)
        if data_output == io.output:
            points = problem.points

        owner = request.user
        try:
            ans = Answer.objects.get(owner=owner, problem=problem)
            ans.output = data_output
            ans.source = data_source
            ans.points = points
            ans.save()
        except Answer.DoesNotExist:
            Answer.objects.create(owner=owner, problem=problem, output=data_output, source=data_source, points=points)

    except:
        raise Http404
    index = post.get('index', 0)
    return HttpResponseRedirect('/codejam/contest/0/dashboard?p=%s' % index)



@require_GET
def input(request, id):
    get = request.GET.copy()
    id = get.get('p', False)
    if not id:
        raise Http404
    io = get.get('io', False)
    if not io:
        raise Http404
    name = get.get('name', False)
    if not name:
        raise Http404

    try:
        io = IO.objects.get(id=io, problem__id=id)
    except IO.DoesNotExist:
        raise Http404

    response = HttpResponse(io.input, mimetype='application/octet-stream', content_type='application/octet-stream')
    # response['Content-Disposition'] = 'attachment; filename="input.txt"'
    response['Content-Disposition'] = 'attachment; filename="%s"' % name
    return response