# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from codejam.apps.account import views as Account
from codejam.apps.contest import views as Contest
from codejam.apps.problem import views as Problem

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import os
basepath = os.path.dirname(__file__)
basepath = os.path.join(basepath, '..', 'codejam_media/static')
basepath = os.path.abspath(basepath)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'codejam.views.home', name='home'),
    # url(r'^codejam/', include('codejam.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'codejam.apps.index'),

    url(r'^accounts/signup/$',  Account.signup),
    url(r'^accounts/login/$',   Account.signin),
    url(r'^accounts/logout/$',  'django.contrib.auth.views.logout_then_login', {'login_url': '/'}),
    url(r'^accounts/profile/$', Account.profile),
    url(r'^accounts/recover/$', Account.recover),
    url(r'^accounts/password/(?P<username>[a-zA-Z0-9]{10}?)/$', Account.change_password),
    
    url(r'^codejam/schedule/$', 'codejam.apps.schedule'),
    url(r'^codejam/terms/$',    'codejam.apps.terms'),
    
    url(r'^codejam/dashboard$', Contest.dashboard),
    
    #url(r'^codejam/contest/(?P<id>\d+?)/dashboard$', Contest.dashboard),
    #url(r'^codejam/contest/(?P<id>\d+?)/dashboard/do$', Contest.dashboard_do),
    #url(r'^codejam/contest/(?P<id>\d+?)/input$', Contest.input),
    #url(r'^codejam/contest/(?P<id>\d+?)/score$', Contest.score),
    #url(r'^codejam/contest/(?P<id>\d+?)/answer$', Contest.answer), # all of answer list
    #url(r'^codejam/contest/(?P<id>\d+?)/source$', Contest.source), # show or download source data
    #url(r'^codejam/contest/(?P<id>\d+?)/output$', Contest.output), # download personal output data

    
    
    #url(r'^codejam/problem/modify$', Problem.modify),
    #url(r'^codejam/problem/delete$', Problem.delete),
    
    #url(r'^codejam/problem/pdf$', Problem.pdf),
    #url(r'^codejam/problem/io$', Problem.io),
)

from codejam import settings
if not settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': basepath})
    )