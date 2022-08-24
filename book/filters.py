import django_filters

from .models import *

class AuthorFilter(django_filters.FilterSet):
    class Meta:
        model = Author
        fields = '__all__'
