from django import template
from cms.models import Category

register = template.Library()

#@register.inclusion_tag('cms/cats.html')
#def get_category_list(cat=None):
    #return {'cats': Category.objects.all(), 'act_cat': cat}