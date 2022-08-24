from django.contrib import admin
from django.utils.safestring import mark_safe

from book.models import Book, BookSearch
from book.models import Author
from book.models import Genre

class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author','cover', 'released', 'date_add','is_published')
    search_fields = ('pk', 'title', 'author','released')
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ('is_published',)
    list_filter = ('is_published', 'date_add')

    def cover(self, object):
        return mark_safe(f"<img src='{object.cover_image.url}'width=50>")

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author_name')
    search_fields = ('pk', 'author_name')
    prepopulated_fields = {"slug":("author_name",)}

class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('pk', 'name')
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Book, BookAdmin)
admin.site.register(BookSearch)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)