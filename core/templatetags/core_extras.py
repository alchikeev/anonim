from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Template filter для получения значения из словаря по ключу"""
    return dictionary.get(key)
