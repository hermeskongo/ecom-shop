from django import template

register = template.Library()


@register.filter
def replace_commas(value):
    return str(value).replace(',', ' ') if value else value
