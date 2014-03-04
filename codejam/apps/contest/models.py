# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from codejam.apps.problem.models import Problem


class Contest(models.Model):
  title = models.CharField(max_length=512)
  visible = models.BooleanField(default=False)
  opened_at = models.DateTimeField(null=False)
  expired_at = models.DateTimeField(null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  closed_at = models.DateTimeField(null=True)
  history = models.TextField(null=True)
  class Meta:
    app_label = u'Contest'
    db_table = u'codejam_contest'
    #order_with_respect_to = 'contest'
    verbose_name = u'Contest'
    verbose_name_plural = u'01 Contest List'

"""
class Answer(models.Model):
  owner = models.ForeignKey(User)
  problem = models.ForeignKey(Problem)
  output = models.TextField()
  source = models.TextField()
  type = models.CharField(max_length=10)
  points = models.IntegerField(default=0)
  updated = models.DateTimeField(auto_now=True)
  class Meta:
    db_table = u'codejam_answer'


class Score(models.Model):
  owner = models.ForeignKey(User)
  points = models.IntegerField(default=0)
  updated = models.DateTimeField(auto_now=True)
  class Meta:
    db_table = u'codejam_score'
"""