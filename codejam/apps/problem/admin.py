# -*- coding: utf-8 -*-
import os.path
from django import forms
from django.contrib import admin
from codejam.apps.contest.models import Contest
from codejam.apps.problem.models import Problem, IO



class ContestChoiceField(forms.ModelChoiceField):
  def label_from_instance(self, obj):
    return obj.title

      

class ProblemForm(forms.ModelForm):

  kr_name = forms.CharField(max_length=256, required=False)
  kr_pdf  = forms.FileField(required=True)
  en_name = forms.CharField(max_length=256, required=False)
  en_pdf  = forms.FileField(required=True)
  
  def clean_kr_pdf(self):
    pdf  = self.cleaned_data.get('kr_pdf')
    name = self.cleaned_data['kr_name']
    if name == None or len(name) == 0:
      name = os.path.splitext(pdf.name)[0]
      self.cleaned_data['kr_name'] = name
    return pdf
  
  def clean_en_pdf(self):
    pdf  = self.cleaned_data.get('en_pdf')
    name = self.cleaned_data['en_name']
    if name == None or len(name) == 0:
      name = os.path.splitext(pdf.name)[0]
      self.cleaned_data['en_name'] = name
    return pdf

  def __init__(self, *args, **kwargs):
    super(ProblemForm, self).__init__(*args, **kwargs)
    self.fields['contest'] = ContestChoiceField(queryset=Contest.objects.all())
    
  class Meta:
    model = Problem



class IO_Inline(admin.StackedInline):
  model = IO
  extra = 1
    
class ProblemAdmin(admin.ModelAdmin):
  list_display = ['get_contest', 'kr_name', 'en_name', 'small_point', 'large_point', 'created_at']
  ordering = ['small_point']
  fieldsets = [
      (None, {'fields': ['contest', 'small_point', 'large_point']})
      , (u'한국어 (이름을 입력하지 않으면 파일 이름이 자동으로 입력 됩니다.)' , {'fields': ['kr_name', 'kr_pdf']})
      , (u'English (If do not fill name field, file name will be copied automatically.)', {'fields': ['en_name', 'en_pdf']})
    ]
  form = ProblemForm
  inlines = [ IO_Inline ]
  
  def get_contest(self, obj):
    return obj.contest.title
  get_contest.short_description = 'Contest'   


admin.site.register(Problem, ProblemAdmin)





class ProblemChoiceField(forms.ModelChoiceField):
  def label_from_instance(self, obj):
    return '%s (%s)' % (obj.kr_name, obj.en_name)



class IOForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(IOForm, self).__init__(*args, **kwargs)
    self.fields['problem'] = ProblemChoiceField(queryset=Problem.objects.all())
    
  class Meta:
    model = IO



class IOAdmin(admin.ModelAdmin):
  list_display = ['get_problem', 'is_large', 'created_at']
  form = IOForm
  
  def get_problem(self, obj):
    return '%s - %s (%s)' % (obj.problem.contest.title, obj.problem.kr_name, obj.problem.en_name)
  get_problem.short_description = 'Problem'


admin.site.register(IO, IOAdmin)









