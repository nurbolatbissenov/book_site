from django.db import models
from django.urls import reverse
from book.models import Author
from book.models.genre import Genre


class Book(models.Model):
    title       = models.CharField(max_length=100)
    slug        = models.SlugField(max_length=100, unique=True, db_index=True,verbose_name='URL')
    cover_image = models.ImageField(upload_to='book/img', blank=True, null=True)
    author      = models.ForeignKey(Author,max_length=50, on_delete=models.CASCADE)
    released    = models.CharField(max_length=10)
    date_add    = models.DateTimeField(verbose_name='date add', auto_now_add=True)
    summary     = models.TextField()
    category    = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')
    is_published = models.BooleanField(default=True)
    pdf         = models.FileField(upload_to='book/pdf')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class BookSearch(models.Model):
    name_of_book = models.CharField(max_length=100)

    def __str__(self):
        return self.name_of_book