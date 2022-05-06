from django import template

register = template.Library()


@register.inclusion_tag('main/components/header.html')
def header(request):
    context = {'request': request}
    return context


@register.inclusion_tag('main/components/sidebar_column.html')
def sidebar_column(request):
    context = {'request': request}
    return context


@register.inclusion_tag('main/components/news_post.html')
def news_post(post):
    context = {'post': post}
    return context


