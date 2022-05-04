from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    image = models.ImageField(null=True, blank=True)
    text = models.CharField(max_length=1000, null=True)


class Comment(models.Model):
    text = models.CharField(max_length=1000, blank=True)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)


class NLUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    tag = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, default='user-avatar.png', blank=True)
    posts = models.ManyToManyField(Post, blank=True, related_name='posts')
    liked_posts = models.ManyToManyField(Post, blank=True, related_name='liked_posts')
    favorite_posts = models.ManyToManyField(Post, blank=True, related_name='favorite_posts')
    comments = models.ManyToManyField(Comment, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name



