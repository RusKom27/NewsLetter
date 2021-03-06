from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.tag

class Post(models.Model):
    image = models.ImageField(null=True, blank=True)
    text = models.CharField(default="", max_length=1000, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id) + " " + str(self.date_created.date())


class Comment(models.Model):
    text = models.CharField(max_length=1000, blank=True)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class NLUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    tag = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, default='user-avatar.png', blank=True)
    posts = models.ManyToManyField(Post, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')
    liked_posts = models.ManyToManyField(Post, blank=True, related_name='liked_posts')
    favorite_posts = models.ManyToManyField(Post, blank=True, related_name='favorite_posts')
    comments = models.ManyToManyField(Comment, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
