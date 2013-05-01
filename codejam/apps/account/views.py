# -*- coding: utf-8 -*-
# Create your views here.
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User



def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
        
    result = {}
    if request.method == 'POST':
        ok = True
        post = request.POST.copy()

        f = post['first_name']
        if len(f) < 1:
            result['first_name'] = '이름을 입력하세요.'
            ok = False

        l = post['last_name']
        if len(l) < 1:
            result['reg_email2_error'] = '성을 입력 하세요.'
            ok = False

        try:
            e1 = post['reg_email1']
            e2 = post['reg_email2']
            from django.core.validators import validate_email
            validate_email(e1)
            if User.objects.filter(email=e1).exists():
                result['reg_email1_error'] = '이미 존재하는 이메일 입니다.'
                ok = False
            elif e1 != e2:
                result['reg_email2_error'] = '이메일이 일치하지 않습니다.'
                ok = False
            else:
                # nothing
                pass
        except:
            result['reg_email1_error'] = '잘못된 형식의 이메일 입니다.'
            ok = False

        p = post['reg_password']
        if len(p) < 6:
            result['reg_password_error'] = '잘못된 비밀번호 입니다.'
            ok = False

        if ok:
            import random
            import string
            c = string.letters + string.digits
            loop = True
            while loop:
                username = ''.join(random.sample(c, 30))
                loop = User.objects.filter(username=username).exists()
            user = User.objects.create_user(username, e1, p)
            user.first_name = f
            user.last_name = l
            user.save()
            
            user = authenticate(username=username, password=p)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/codejam/contest/0/dashboard')
            
        result['last_name'] = post['last_name']
        result['first_name'] = post['first_name']
        result['reg_email1'] = post['reg_email1']
        result['reg_email2'] = post['reg_email2']

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
        except User.DoesNotExist:
            pass
        result['email'] = post['email']
        result['persist'] = persist
    variables = RequestContext(request, result)
    return render_to_response('account/login.html', variables)





@login_required
def profile(request):
    pass

def recover(request):
    pass