from django import template
from book.models import *

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Genre.objects.all()
    else:
        return Genre.objects.filter(pk=filter)

@register.inclusion_tag('book/list_category.html')
def show_categories(sort=None, category_selected=0):
    if not sort:
        category = Genre.objects.all()
    else:
        category = Genre.objects.order_by(sort)

    return {"category": category, "category_selected": category_selected}
