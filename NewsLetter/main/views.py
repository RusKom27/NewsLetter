from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import FileSystemStorage

from collections import Counter

from .forms import CustomUserCreationForm, NLUserCreationForm
from .models import *
from .decorators import unauthenticated_user


def get_request_data(request, name):
    if name in request.GET and request.GET[name] != '':
        return request.GET[name]
    else:
        return ''


def get_posts(request, author='all', tag='all', favorites=False):
    posts = []
    liked_posts = []
    if author == 'all':
        users = User.objects.all()
    else:
        users = [author]
    for user in users:
        for post in user.nluser.liked_posts.all():
            liked_posts.append(post.id)
        if favorites:
            for fav_post in request.user.nluser.favorite_posts.all():
                for post in user.nluser.posts.filter(id=fav_post.id):
                    posts.append({'author': user, 'content': post, 'likes': 0})
        if tag == 'all':
            for post in user.nluser.posts.all():
                posts.append({'author': user, 'content': post, 'likes': 0})
        elif tag != "":
            for post in user.nluser.posts.filter(tags=Tag.objects.filter(tag=tag)[0]):
                posts.append({'author': user, 'content': post, 'likes': 0})
    id_likes = dict(Counter(liked_posts))
    for post in posts:
        for (key, value) in id_likes.items():
            if post['content'].id == key:
                post.update({'likes': value})

    def get_datetime(e):
        return e['content'].date_created

    posts.sort(reverse=True, key=get_datetime)
    return posts


def create_post(request):
    post_text = request.POST.get('text')

    if "image" in request.FILES:
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        post_image = fss.url(file)
    else:
        post_image = ""

    if post_text == "" and post_image == "":
        print("Post data is empty!")
        return "Post data is empty!"

    user_posts = request.user.nluser.posts
    if len(user_posts.filter(text=post_text)) < 1 and post_text != "":
        post = Post.objects.create()
        if post_image != "":
            post.image = post_image
        post.text = post_text
        words = post_text.split(' ')
        for word in words:
            if '#' in word:
                tag_words = word.split('#')
                for i in range(len(tag_words)):
                    if i == 0:
                        pass
                    else:
                        tags = Tag.objects.filter(tag=tag_words[i])
                        if len(tags) < 1:
                            tag = Tag.objects.create(tag=tag_words[i])
                        else:
                            tag = tags[0]
                        post.tags.add(tag)
        post.save()
        request.user.nluser.posts.add(post)


def main(request):
    posts = get_posts(request, 'all')
    if request.user.is_authenticated:
        request.user.nluser.tags.set(Tag.objects.all())

    tag = get_request_data(request, "tag")
    if tag != "":
        posts = get_posts(request, "all", tag)

    context = {'title': 'Главная | #' + tag,
               'posts': posts}

    return render(request,
                  'main/pages/main.html',
                  context)


def favorite_posts(request):
    posts = get_posts(request, tag="", favorites=True)

    context = {'title': 'Избранное',
               'posts': posts}

    return render(request,
                  'main/pages/favorite_posts.html',
                  context)


@login_required(login_url='auth')
def cabinet(request):
    posts = get_posts(request, request.user)
    context = {'title': request.user.nluser.name + '(' + request.user.nluser.tag + ')',
               'posts': posts}
    if request.method == 'POST' and "image" in request.FILES:
        create_post(request)
    elif request.method == 'POST':
        create_post(request)
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


@login_required(login_url='auth')
def set_like(request):
    if len(request.user.nluser.liked_posts.filter(id=request.GET['like'])) == 0:
        request.user.nluser.liked_posts.add(Post.objects.filter(id=request.GET['like'])[0])
    else:
        request.user.nluser.liked_posts.remove(Post.objects.filter(id=request.GET['like'])[0])
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='auth')
def save_post(request):
    if len(request.user.nluser.favorite_posts.filter(id=request.GET['save_post'])) == 0:
        request.user.nluser.favorite_posts.add(Post.objects.filter(id=request.GET['save_post'])[0])
    else:
        request.user.nluser.favorite_posts.remove(Post.objects.filter(id=request.GET['save_post'])[0])
    return redirect(request.META.get('HTTP_REFERER'))


def unknown(request):
    return redirect('main')

