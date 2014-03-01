# -*- coding: utf-8 -*-
# Create your views here.
import re
import string
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext



def __check_name(first_name, last_name):
  ok = True
  result = {}

  if len(first_name) < 1:
    result['first_name_error'] = '이름을 입력하세요.'
    ok = False
  if len(last_name) < 1:
    result['last_name_error'] = '성을 입력 하세요.'
    ok = False
    
  return ok, result



def __check_email(email1, email2):
  ok = False
  result = {}

  try:
    from django.core.validators import validate_email
    validate_email(email1)

    from codejam.settings import LGEMAIL_ONLY
    if LGEMAIL_ONLY:
      p = re.compile('^(?P<name>.*)@lge.com$')
    else:
      p = re.compile('^(?P<name>.*)@([^@]+)$')
    m = p.match(email1)

    if m == None:
      result['reg_email1_error'] = 'LG전자의 이메일이 아닙니다.'
    elif email1 != email2:
      result['reg_email2_error'] = '이메일이 일치하지 않습니다.'
    elif User.objects.filter(email=email1).exists():
      result['reg_email1_error'] = '이미 존재하는 이메일 입니다.'
    else:
      result['username'] = m.group('name')
      ok = True
  except:
      result['reg_email1_error'] = '잘못된 형식의 이메일 입니다.'

  return (ok, result)



def __check_password(password1, password2):  
  ok = True
  result = {}

  if len(password1) < 6:
    result['reg_password_error1'] = '안전하지 않은 비밀번호 입니다.'
    ok = False
  
  if ok and (password1 != password2):
    result['reg_password_error2'] = '두 비밀번호가 일치하지 않습니다.'
    ok = False

  return (ok, result)



def __make_username():
  c = string.letters + string.digits
  loop = True
  while loop:
    username = ''.join(random.sample(c, 10))
    loop = User.objects.filter(username=username).exists()
  return username



def __create_user(email, first_name, last_name):
  username = __make_username()
  user = User.objects.create_user(username, email)
  user.first_name = first_name
  user.last_name = last_name
  user.set_unusable_password()
  user.is_active = True
  user.save()
  return user



def __get_reg_password_email_body(host, username, recover=False):
  from django.template import Context, loader
  t = loader.get_template('account/change_password_email.body')
  c = Context({'host': host, 'username': username, 'recover': recover})
  return t.render(c)



def signup(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  
  result = {}
  if request.method == 'POST':
    post = request.POST.copy()

    f = post['first_name']
    l = post['last_name']
    e1 = post['reg_email1']
    e2 = post['reg_email2']
  
    ok, result = __check_name(f, l)
    if ok:
      ok, result = __check_email(e1, e2)
    if ok:
      user = __create_user(e1, f, l)
      host = request.META['HTTP_HOST']
      message = __get_reg_password_email_body(host, user.username)
      subject = 'codejam 가입을 완료해 주세요.'
      user.email_user(subject, message)
      return render(request, 'account/email_delivery_complete.html')
        
    result['last_name'] = l
    result['first_name'] = f
    result['reg_email1'] = e1
    result['reg_email2'] = e2

  variables = RequestContext(request, result)
  return render_to_response('account/signup.html', variables)



def signin(request):

  if request.user.is_authenticated():
    return HttpResponseRedirect('/codejam/contest/0/dashboard')

  result ={}
  if request.method == 'POST':
    post = request.POST.copy()
    persist = ('persist' in post) and post['persist'] == 'on'
    try:
      username = User.objects.get(email=post['email']).username
      user = authenticate(username=username, password=post['password'])
      if user is not None and user.is_active:
        if persist:
            pass
        post.update({'username': username})
        request.POST = post
        login(request, user)
        return HttpResponseRedirect('/codejam/contest/0/dashboard')
      else:
        result['error'] = '비밀번호를 다시 확인해 주세요.'
    except User.DoesNotExist:
      result['error'] = '등록되지 않은 이메일 입니다.'

    result['email'] = post['email']
    result['persist'] = persist

  variables = RequestContext(request, result)
  return render_to_response('account/signin.html', variables)



@login_required
def profile(request):
  pass



def recover(request):

  result = {'recover': True}

  if request.method == 'POST':
    e = request.POST['email']
    result['email'] = e
    try:
      u = User.objects.get(email=e)
      u.username = __make_username()
      u.save()

      host = request.META['HTTP_HOST']
      message = __get_reg_password_email_body(host, u.username, True)
      subject = 'codejam 비밀번호를 변경해 주세요.'
      u.email_user(subject, message)
      
      return render(request, 'account/email_delivery_complete.html', result)
    except User.DoesNotExist:
      result['error'] = True

  variables = RequestContext(request, result)
  return render_to_response('account/recover.html', variables)



def change_password(request, username):

  try:
    user = User.objects.get(username=username)
  except:
    raise Http404

  variables = {'username': username}

  if request.method == 'POST':
    post = request.POST.copy()

    p1 = post['reg_password1']
    p2 = post['reg_password2']
    ok, result = __check_password(p1, p2)

    if not ok:
      variables.update(result)
      return render(request, 'account/change_password.html', variables)

    user.username = __make_username()
    user.set_password(p1)
    user.is_active = True
    user.save()
    
    return HttpResponseRedirect('/')
  
  return render(request, 'account/change_password.html', variables)