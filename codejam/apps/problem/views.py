# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime, timedelta
from django.db.models import Sum
from django.core.serializers import serialize
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required

from codejam.settings import MEDIA_ROOT
from codejam.apps.contest.models import Score
from codejam.apps.problem.models import Problem, IO, TempDataSet, Answer
#from codejam.apps.problem.models import IO



@require_POST
@login_required
def ajax_answer(request):
  
  update_score = False
  variables = { 'ok': False }
  post = request.POST.copy()

  try:
    p = Problem.objects.get(id=post['problem'])
    t = TempDataSet.objects.get(id=post['input']
                                , owner=request.user
                                , expired_at__gte=datetime.now())

    lhs = post['answer'].replace('\r\n', ' ').replace('\n\r', ' ').replace('\n', ' ').replace('\r', ' ').strip().split(' ')
    rhs = t.output.replace('\r\n', ' ').replace('\n\r', ' ').replace('\n', ' ').replace('\r', ' ').strip().split(' ')
    
    is_large = (post['type'] == 'large')
    a = Answer.objects.get_or_create(owner=request.user
                                     , problem=p
                                     , is_large=is_large)[0]
    a.try_count = a.try_count + 1
    if a.complete_at == None:
      if lhs == rhs:
        a.complete_at = datetime.now()
        if is_large:
          a.points = p.large_point
        else:
          a.points = p.small_point
        update_score = True
      else:
        a.failed_count = a.failed_count + 1
    a.save()
    
    userdata = json.loads(t.userdata)
    userdata.append({ 'ok': lhs == rhs, 'timestamp': str(datetime.now()), 'output': post['answer'] })
    t.userdata = json.dumps(userdata)
    t.save()

    if lhs == rhs:
      variables['ok'] = True
    else:
      variables['error'] = 'wrong answer.'
      
    if update_score:
      c = p.contest
      s = Score.objects.get_or_create(owner=request.user, contest=c)[0]
      t = Answer.objects.filter(owner=request.user, problem__contest=c).aggregate(Sum('points'), Sum('failed_count'))
      s.points = t['points__sum']
      s.failed = t['failed_count__sum']
      s.save()

  except Problem.DoesNotExist:
    return HttpResponseBadRequest()
  except TempDataSet.DoesNotExist:
    return HttpResponseBadRequest()

  return HttpResponse(json.dumps(variables), content_type='application/json')



@require_POST
@login_required
def ajax_get_input_id(request):

  post = request.POST.copy()

  pid = post['problem']
  is_large = post['type'] == 'large'

  ds = IO.objects.filter(problem_id=pid, is_large=is_large)
  idx = random.randint(0, len(ds)-1)
  d = ds[idx]

  expired  = datetime.now() + timedelta(minutes=10)
  d = TempDataSet.objects.create(owner        = request.user
                                 , problem_id = pid
                                 , is_large   = is_large
                                 , input      = d.input
                                 , output     = d.output
                                 , expired_at = expired)

  return HttpResponse(d.id, content_type='plain/text')

  

@require_GET
@login_required
def download_input(request, id, name):
  t = TempDataSet.objects.get(id=id)
  r = HttpResponse(t.input, content_type='application/octet-stream')
  r['Content-Disposition'] = 'attachment; filename="%s"' % name
  return r



@require_GET
@login_required
def download_pdf(request, id, language):
  p = Problem.objects.get(id=id)

  if language == 'kr':
    f = p.kr_pdf
  elif language == 'en':
    f = p.en_pdf
  else:
    return HttpResponseBadRequest()

  r = HttpResponse(f.file.read(), content_type='application/octet-stream')
  r['Content-Disposition'] = 'attachment; filename="%s"' % os.path.split(f.name)[1].encode('utf-8')
  return r


"""
@login_required
def list(request):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404
    
    result = {}

    if request.method == 'POST':
        success, value = Create(request)
        if success:
            return HttpResponseRedirect('/codejam/problem/modify?p=%d' % value)
        else:
            result['error'] = value

    result['problems'] = Problem.objects.all().values()
    variables = RequestContext(request, result)
    return render_to_response('problem/list.html', variables)
  
  

def Create(request):

    post = request.POST.copy()
    files = request.FILES.copy()
    
    name = post.get('name', False)
    if not name:
        return (False, 'There is no name.')

    if Problem.objects.filter(name=name).exists():
        return (False, "Problem already exists.")

    pdf = files.get('pdf', False)
    if not pdf:
        return (False, 'There is no pdf file.')

    points = post.get('points', False)
    if not points:
        return (False, 'There is no points.')

    pdf_name = pdf.name
    filename = os.path.splitext(pdf_name)[0]

    dirpath = os.path.join(MEDIA_ROOT, filename)
    pdf_path = os.path.join(dirpath, pdf_name)

    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    if not os.path.isdir(dirpath) or os.path.exists(pdf_path):
        return (False, "Server Error. Please change PDF name.")
    fp = open(pdf_path, 'wb')
    for chunk in pdf.chunks():
        fp.write(chunk)
    fp.close()

    rel_path = os.path.join(filename, pdf_name)
    p = Problem.objects.create(name=name, pdf=rel_path, points=points)
    return (True, p.id)





def MakeShortString(string):
    pos = 0
    for i in range(0, 4):
        pos = string.find('\n', pos+1)
        if pos == -1:
            break
    if pos != -1:
        string = string[:pos] + '\n......'
    return string

@login_required
def modify(request):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404
    
    r = request.REQUEST.copy()
    
    id = r.get('p', False)
    if not id:
        raise Http404
    try:
        p = Problem.objects.get(id=id)
    except Problem.DoesNotExist:
        raise Http404

    result = {'id': id, 
              'name': p.name, 
              'pdf': os.path.split(p.pdf)[1],
              'points': p.points}
    
    ios = IO.objects.filter(problem__id=id).values()
    for i in range(0, len(ios)):
        ios[i]['input'] = MakeShortString(ios[i]['input'])
        ios[i]['output'] = MakeShortString(ios[i]['output'])
    result['ios'] = ios
    
    if request.method == 'GET':
        variables = RequestContext(request, result)
        return render_to_response('contest/problem_modify.html', variables)
    else: # POST
        is_valid = True

        points = r.get('points', False)
        if not points:
            points = p.points
            is_valid = False
        result['points'] = points

        if is_valid:
#            p.name = name
            p.points = points
            pdf = request.FILES.get('pdf', False)
            if pdf:
                org_path = os.path.join(MEDIA_ROOT, p.pdf)
                dir_path = os.path.dirname(org_path)

                pdf_path = os.path.join(dir_path, pdf.name)

                fp = open(pdf_path, 'wb')
                for chunk in pdf.chunks():
                    fp.write(chunk)
                fp.close()

                rel_path = os.path.join(os.path.split(dir_path)[1], pdf.name)
                p.pdf = rel_path
                
                result['pdf'] = pdf.name
                os.remove(org_path)

            p.save()
        else:
            result['error'] = 'Not enough arguments.'

        variables = RequestContext(request, result)
        return render_to_response('contest/problem_modify.html', variables)



def RemoveAll(root):
    for base, dirs, files in os.walk(root, topdown=True):
        for name in files:
            os.remove(os.path.join(base, name))
        for name in dirs:
            dir = os.path.join(base, name)
            RemoveAll(dir)
        os.rmdir(root)
    
@require_GET
@login_required
def delete(request):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404
    
    get = request.GET.copy()
    try:
        p = Problem.objects.get(id=get['p'])
        filepath = os.path.join(MEDIA_ROOT, p.pdf)
        RemoveAll(os.path.dirname(filepath))
        p.delete()
    except:
        raise Http404
    return HttpResponseRedirect('/codejam/problem')



@require_GET
def pdf(request):
    get = request.GET.copy()
    id = get.get('p', False)
    if not id:
        raise Http404
    try:
        pdf = Problem.objects.get(id=id).pdf
    except Problem.DoesNotExist:
        raise Http404
    response = serve(request, pdf, MEDIA_ROOT, False)
    name = get.get('name', os.path.split(pdf)[1])
    response['Content-Disposition'] = 'attachment; filename="%s"' % name 
    response['content-type'] = 'application/octet-stream'
    return response



@require_POST
@login_required
def IOInsert(request, id):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404
    
    post = request.POST.copy()
    try:
        p = Problem.objects.get(id=id)
    except Problem.DoesNotExist:
        raise Http404

    i = post.get('input', False)
    o = post.get('output', False)

    result = {}
    if not i:
        if o:
            result['output'] = o
        return False
    result['input'] = i
    
    if not o:
        return False
    result['output'] = o

    i = i.replace('\r\n', '\n')
    o = o.replace('\r\n', '\n')
    IO.objects.create(problem=p, input=i, output=o)
    return True

@require_GET
@login_required
def IOPreview(request, id):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404
    
    get = request.GET.copy()
    try:
        io = IO.objects.get(problem__id=id, id=get['io'])
    except:
        raise Http404
    return io

@require_GET
@login_required
def IODelete(request, id):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404
    
    get = request.GET.copy()
    try:
        IO.objects.get(problem__id=id, id=get['io']).delete()
    except:
        raise Http404
    
def io(request):
    r = request.REQUEST.copy()
    id = r.get('p', False)
    if not id:
        raise Http404
    cmd = r.get('cmd', False)
    if not cmd:
        raise Http404

    result = {'id': id}
    if cmd == 'Insert':
        success = IOInsert(request, id);
        if success:
            res = HttpResponseRedirect('/codejam/problem/modify?p=%s' % id)
        else:
            res = HttpResponseBadRequest() 
    elif cmd == 'Preview':
        result['io'] = IOPreview(request, id)
        variables = RequestContext(request, result)
        return render_to_response('contest/problem_io_preview.html', variables)
    elif cmd == 'Delete':
        IODelete(request, id)
        res = HttpResponseRedirect('/codejam/problem/modify?p=%s' % id)
    else:
        raise Http404
    return res
"""
