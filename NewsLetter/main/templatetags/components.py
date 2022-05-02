from django import template

register = template.Library()


@register.inclusion_tag('main/components/header.html')
def header():
    return


@register.inclusion_tag('main/components/primary_column.html')
def primary_column(page):
    context = {'page': page}
    return context


@register.inclusion_tag('main/components/sidebar_column.html')
def sidebar_column():
    return


@register.inclusion_tag('main/components/news_block.html')
def news_block():
    return
