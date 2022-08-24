from django.db import models


class Author(models.Model):
    author_name = models.CharField('Author', max_length=100, db_index=True, unique=False)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.author_name
