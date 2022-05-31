from django import template
from django.views.generic import DetailView

register = template.Library()


@register.inclusion_tag('main/components/header.html', takes_context=True)
def header(context, request):
    return {"context": context, "request": request}


@register.inclusion_tag('main/components/sidebar_column.html', takes_context=True)
def sidebar_column(context, request):
    return {"context": context, "request": request}


@register.inclusion_tag('main/components/news_post.html')
def news_post(post):
    context = {'post': post}
    return context

