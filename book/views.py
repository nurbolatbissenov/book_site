from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, request
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from book.models import *
from .filters import AuthorFilter
from .forms import RegisterUserForm, LoginUserForm
from .utils import *

class BookHome(DataMixin, ListView):
    model = Book
    template_name = 'book/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Book.objects.filter(is_published=True).select_related('category')

def about(request):
    contact_list = Book.objects.all()
    paginator = Paginator(contact_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'book/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


def about(request):
    return render(request, 'book/about.html', {'menu': menu, 'title': 'О сайте'})

def contact(request):
    return HttpResponse("Обратная связь")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DataMixin, DetailView):
    model = Book
    template_name = 'book/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class BookCategory(Genre,DataMixin,ListView):
    model = Book
    template_name = 'book/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Book.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['filter'] = AuthorFilter(self.request.Get, queryset=self.get_queryset())
        c = Genre.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      category_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin,CreateView):
    form_class = RegisterUserForm
    template_name = 'book/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin,LoginView):
    form_class = LoginUserForm
    template_name = 'book/login.html'

    def get_context_data(self,*, object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

# class Search(ListView):
#     model = Book
#
#     def get_queryset(self):
#         return Book.objects.filter(title__icontains=self.request.GET.get("search_book"))
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["search"] = self.request.GET.get("search")
#         return context

# class Search(ListView):
#     model = Book
#     template_name = 'base.html'
#
#     def get_queryset(self):
#         query = self.request.GET.get("search_book")
#         object_list = Book.objects.filter(title__icontains=query)
#         return object_list

def search(request):
    search_book = request.GET.get('search_book')
    if search_book:
        posts = Book.objects.filter(Q(title__icontains=search_book) & Q(content__icontains=search_book))

    return render(request, 'base.html', {'posts': posts})

