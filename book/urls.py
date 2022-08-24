from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', BookHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    #path('search/', Search.as_view(), name='search'),
    path('search/', views.search, name='search'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:category_slug>/', BookCategory.as_view(), name='category'),
]