# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter(name='deco')
def __to_upper__(value):
  return chr(65 + value)

@register.filter(name='suffix_small')
def __suffix_small__(value):
  return (2 * value)

@register.filter(name='suffix_large')
def __suffix_large__(value):
  return (2 * value + 1)