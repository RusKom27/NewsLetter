from django import template

register = template.Library()


@register.inclusion_tag('main/pages/main.html')
def main():
    return


@register.inclusion_tag('main/pages/cabinet.html')
def cabinet():
    return


@register.inclusion_tag('main/pages/registration.html')
def registration():
    return


@register.inclusion_tag('main/pages/login.html')
def login():
    return