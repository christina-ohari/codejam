# -*- coding: utf-8 -*-
import os.path
from django.db import models
from django.contrib.auth.models import User
from codejam.apps.contest.models import Contest



class Problem(models.Model):
  contest = models.ForeignKey(Contest)
  kr_name = models.CharField(max_length=256, null=True)
  kr_pdf  = models.FileField(upload_to='problem')
  en_name = models.CharField(max_length=256, null=True)
  en_pdf  = models.FileField(upload_to='problem')
  small_point = models.IntegerField(default=0)
  large_point = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  class Meta:
    app_label = u'problem'
    db_table = u'codejam_problem'
    #order_with_respect_to = 'contest'
    verbose_name = u'Problem'
    verbose_name_plural = u'01 Problem List'



class IO(models.Model):
  problem  = models.ForeignKey(Problem)
  is_large = models.BooleanField(default=False)
  input    = models.TextField()
  output   = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  class Meta:
    app_label = u'problem'
    db_table = u'codejam_problem_io'
    #order_with_respect_to = 'problem'
    verbose_name = u'Problem Input/Output'
    verbose_name_plural = u'02 Problem Input/Output List'



class Answer(models.Model):
  owner     = models.ForeignKey(User)
  problem   = models.ForeignKey(Problem)
  small_complete_at  = models.DateTimeField(null=True, default=None)
  small_failed_count = models.IntegerField(default=0)
  large_complete_at  = models.DateTimeField(null=True, default=None)
  large_failed_count = models.IntegerField(default=0)
  history   = models.TextField(default='[]')
  try_count = models.IntegerField(default=0)
  points    = models.IntegerField(default=0)
  class Meta:
    app_label = u'problem'
    db_table  = u'codejam_answer'
    #order_with_respect_to = 'contest'
    verbose_name = u'Answer'
    verbose_name_plural = u'03 Answer List'