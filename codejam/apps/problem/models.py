# -*- coding: utf-8 -*-
import os.path
from django.db import models


class Problem(models.Model):
    name   = models.CharField(max_length=256, null=True)
    pdf    = models.CharField(max_length=256, null=True)
    points = models.IntegerField(default=0)
    class Meta:
        db_table = u'codejam_problem'

class IO(models.Model):
    problem = models.ForeignKey(Problem)
    input   = models.TextField()
    output  = models.TextField()
    class Meta:
        db_table = u'codejam_problem_io'