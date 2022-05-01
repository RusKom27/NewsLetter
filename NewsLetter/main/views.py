from django.shortcuts import render
from .models import *


def index(request):
    context = {'title': 'Main'}

    return render(request,
                  'main/index.html',
                  context)