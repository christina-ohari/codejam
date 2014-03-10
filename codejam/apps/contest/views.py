# -*- coding: utf-8 -*-
import os.path
from datetime import datetime
from django.db.models import Q
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from codejam.apps.contest.models import Contest
#from codejam.apps.contest.models import Answer
#from codejam.apps.contest.models import Score
#from codejam.apps.problem.models import Problem
#from codejam.apps.problem.models import IO



@require_GET
@login_required
def dashboard(request):
  
  variables = {}
  
  try:
    today = datetime.today()
    q = Q(opened_at__lte=today) & Q(expired_at__gte=today) & Q(visible=True)
    contest = Contest.objects.get(q)
    problem_list = contest.problem_set.all().values()
    variables.update({
        'contest': contest,
        'problems': problem_list
      })

    print problem_list
    
  except Contest.DoesNotExist:
    print 'no-contest'
    pass

  return render(request, 'contest/dashboard.html', variables)


"""
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

    #answer = files.get('answer', False)
    answer = post.get('answer', False)
    if not answer:
        # return HttpResponseBadRequest()
        raise Http404
    #source = files.get('source', False)
    source = post.get('source', False)
    if not source:
        # return HttpResponseBadRequest()
        raise Http404
        

    try:
        io = IO.objects.get(id=input, problem__id=id)

        owner = request.user
        
        points = 0
        problem = Problem.objects.get(id=id)
        lhs = answer.replace('\r', ' ').replace('\n', ' ').split(' ')
        try:
            while True:
                lhs.remove('')
        except:
            pass
        rhs = io.output.replace('\r', ' ').replace('\n', ' ').split(' ')
        try:
            while True:
                rhs.remove('')
        except:
            pass

        ext = os.path.splitext(source.name)[1]
        try:
            ans = Answer.objects.get(owner=owner, problem=problem)
            ans.output = data_output
            ans.source = data_source
            ans.type = ext
            ans.points = points
            ans.save()
        except Answer.DoesNotExist:
            Answer.objects.create(owner=owner, problem=problem, output=data_output, source=data_source, type=ext, points=points)

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



@require_GET
def score(request, id):
    get = request.GET.copy()
    
    from django.db.models import Sum, Max
    from django.contrib.auth.models import User
    q = User.objects.annotate(points=Sum('answer__points'))
    q = q.annotate(updated=Max('answer__updated'))
    q = q.filter(points__gt=0)
    q = q.order_by('-points', 'updated')
    scores = q.values('email', 'points', 'updated')
    end = get.get('max', -1)
    if end != -1 and end < len(scores):
        scores = scores[:end]

    variables = RequestContext(request, {'scores': scores})
    return render_to_response('contest/dashboard_score.html', variables)



@require_GET
def answer(request, id):
    answers = Answer.objects.all().order_by('-points', '-updated')
    answers = answers.values('owner__email', 'problem__name', 'id', 'points', 'updated')
    variables = RequestContext(request, {'answers': answers})
    return render_to_response('contest/dashboard_answer.html', variables)




@require_GET
@login_required
def source(request, id):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404
    
    get = request.GET.copy()

    cmd = get.get('cmd', False)
    if not cmd:
        raise Http404
    
    id = get.get('s', False)
    if not id:
        raise Http404
    
    try:
        ans = Answer.objects.get(id=id)
    except Answer.DoesNotExist:
        raise Http404
    
    name = ans.owner.email
    name = name[:name.find('@')]
    filename = '%s-%s-source%s' % (name, ans.problem.name, ans.type)

    if cmd == 'Show':
        brush = {'.c': 'c',
                 '.cpp': 'cpp',
                 '.cxx': 'cpp',
                 '.js' : 'java',
                 '.py' : 'py',
                 '.rb' : 'ruby',
                 '.rbw': 'ruby'}
        result = {'id': ans.id,
                  'owner':ans.owner.email,
                  'problem': ans.problem.name,
                  'filename': filename, 
                  'src': ans.source,
                  'brush': brush.get(ans.type, 'text')}
        variables = RequestContext(request, result)
        return render_to_response('contest/dashboard_source.html', variables)
    elif cmd == 'Download':
        
        response = HttpResponse(ans.source, mimetype='application/octet-stream', content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
    else:
        raise Http404



@require_GET
@login_required
def output(request, id):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404
    
    get = request.GET.copy()

    id = get.get('s', False)
    if not id:
        raise Http404
    
    try:
        ans = Answer.objects.get(id=id)
    except Answer.DoesNotExist:
        raise Http404
    
    name = ans.owner.email
    name = name[:name.find('@')]
    filename = '%s-%s-output.txt' % (name, ans.problem.name)
    
    response = HttpResponse(ans.output, mimetype='application/octet-stream', content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response
"""