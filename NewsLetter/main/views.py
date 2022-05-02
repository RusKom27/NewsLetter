from django.shortcuts import render, redirect
from .models import *


def index(request):
    if 'page' in request.GET and request.GET['page'] != '':
        page = request.GET['page']
    else:
        page = 'main'

    context = {'title': 'Main',
               'page': page}

    return render(request,
                  'main/index.html',
                  context)
