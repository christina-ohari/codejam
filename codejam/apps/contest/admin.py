# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.contrib import admin
from codejam.apps.contest.models import Contest, Score



class ContestForm(forms.ModelForm):
  
  closed_at = forms.BooleanField(required=False)

  def clean_visible(self):
    data = self.cleaned_data['visible']
    if data and Contest.objects.filter(visible=True).exists:
      raise forms.ValidationError('이미 활성화 된 코드잼이 존재합니다.')
    return data

  def clean_expired_at(self):
    expired = self.cleaned_data['expired_at']
    opened = self.cleaned_data['opened_at']
    if opened < expired:
      return expired
    raise forms.ValidationError('종료일이 시작일보다 과거입니다.')

  def clean_closed_at(self):
    data = self.cleaned_data['closed_at']
    if data == None or data == False:
      return None
    return datetime.today() 

  class Meta:
    model = Contest



class Score_Inline(admin.TabularInline):
  model = Score
  readonly_fields = ('owner', 'points', 'updated', 'failed')
  ordering = ['-points', '-updated', 'failed']
  can_delete = False
  extra = 0
  def has_add_permission(self, request):
    return False
  def get_owner(self):
    return 'a'

class ContestAdmin(admin.ModelAdmin):
  list_display = ['title', 'visible', 'opened_at', 'expired_at', 'closed_at']
  ordering = ['opened_at']
  fieldsets = [
      (None, {'fields': ['title', 'visible']})
      , ('코드잼 기간' , {'fields': ['opened_at', 'expired_at']})
      , ('코드잼 닫기 (visible이 Ture 일 경우 history가 공개됩니다.)', {'fields': ['closed_at']})
    ]
  form = ContestForm
  inlines = [ Score_Inline ]


admin.site.register(Contest, ContestAdmin)





class ScoreAdmin(admin.ModelAdmin):
  pass


admin.site.register(Score, ScoreAdmin)