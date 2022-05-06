import http.client

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from collections import Counter

from .forms import CustomUserCreationForm, NLUserCreationForm
from .models import *
from .decorators import unauthenticated_user


def get_request_data(request, name):
    if name in request.GET and request.GET[name] != '':
        return request.GET[name]
    else:
        return ''


def get_posts(author='all'):
    posts = []
    liked_posts = []
    if author == 'all':
        users = User.objects.all()
    else:
        users = [author]
    for user in users:
        for post in user.nluser.liked_posts.all():
            liked_posts.append(post.id)
        for post in user.nluser.posts.all():
            posts.append({'author': user, 'content': post, 'likes': 0})
    id_likes = dict(Counter(liked_posts))
    for post in posts:
        for (key, value) in id_likes.items():
            if post['content'].id == key:
                post.update({'likes': value})
    return posts


def main(request):
    posts = get_posts('all')
    context = {'title': 'Главная',
               'posts': posts}

    return render(request,
                  'main/pages/main.html',
                  context)


@login_required(login_url='auth')
def cabinet(request):
    posts = get_posts(request.user)
    context = {'title': request.user.nluser.name + '(' + request.user.nluser.tag + ')',
               'posts': posts}
    if request.method == 'POST':
        post_text = request.POST.get('text')
        post = Post.objects.create()
        if request.POST.get('text') != '':
            post.text = post_text
        if request.POST.get('image') != '':
            post.image = request.POST.get('image')
        words = post_text.split(' ')
        for word in words:
            if '#' in word:
                tag_words = word.split('#')
                for i in range(len(tag_words)):
                    if i == 0:
                        pass
                    else:
                        tag = Tag.objects.create(tag=tag_words[i])
                        post.tags.add(tag)

        post.save()
        request.user.nluser.posts.add(post)
    if get_request_data(request, 'user_tag') == request.user.nluser.tag:
        return render(request,
                      'main/pages/cabinet.html',
                      context)
    else:
        return render(request,
                      'main/pages/cabinet.html',
                      context)


@unauthenticated_user
def registration(request):
    error = ''
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='NLUser')
            user.groups.add(group)
            NLUser.objects.create(
                name=user.username,
                email=user.email,
                user=user,
                tag='@' + user.email.split("@")[0]
            )

            return redirect('auth')
        else:
            error = 'Неправильный ввод!'
            print(error)

    context = {'error': error,
               'title': 'Регистрация',
               'form': form}

    return render(request,
                  'main/pages/registration.html',
                  context)


@unauthenticated_user
def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')

    context = {'page': 'auth',
               'title': 'Вход'}

    return render(request,
                  'main/pages/auth.html',
                  context)


@login_required(login_url='auth')
def unauth(request):
    logout(request)
    return redirect('auth')


def set_like(request):
    if len(request.user.nluser.liked_posts.filter(id=request.GET['like'])) == 0:
        request.user.nluser.liked_posts.add(Post.objects.filter(id=request.GET['like'])[0])
    else:
        request.user.nluser.liked_posts.remove(Post.objects.filter(id=request.GET['like'])[0])
    return redirect(request.META.get('HTTP_REFERER'))


def unknown(request):
    return redirect('main')

