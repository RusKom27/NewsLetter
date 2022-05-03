from django.shortcuts import render, redirect
from .models import *


def get_request_data(request, name):
    if name in request.GET and request.GET[name] != '':
        return request.GET[name]
    else:
        return ''


def index(request):
    page = get_request_data(request, 'page')

    data = get_request_data(request, 'form')

    context = {'title': 'Main',
               'page': page}

    return render(request,
                  'main/index.html',
                  context)
