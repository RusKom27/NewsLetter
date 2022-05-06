from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('auth', views.auth, name='auth'),
    path('registration', views.registration, name='registration'),

    path('unauth', views.unauth, name='unauth'),
    path('set_like', views.set_like, name='set_like'),

    re_path('', views.unknown)
]

