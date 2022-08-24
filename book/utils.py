from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

class DataMixin:
        paginate_by = 3

        def get_user_context(self, **kwargs):
                context = kwargs
                #category = Genre.objects.annotate(Count('book'))
                category = cache.get('category')
                if not category:
                    category = Genre.objects.all()
                    cache.set(category, category, 60)

                context['menu'] = menu

                context['category'] = category
                if 'category_selected' not in context:
                        context['category_selected'] = 0
                return context