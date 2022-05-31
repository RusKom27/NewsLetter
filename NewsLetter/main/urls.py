from django.urls import path, re_path
from . import views


urlpatterns = [
    path('main', views.main, name='main'),
    path('', views.main, name='main'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('favorite_posts', views.favorite_posts, name='favorites'),
    path('auth', views.auth, name='auth'),
    path('registration', views.registration, name='registration'),

    path('unauth', views.unauth, name='unauth'),
    path('set_like', views.set_like, name='set_like'),
    path('save_post', views.save_post, name='save_post'),
]

