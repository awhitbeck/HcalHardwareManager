from django import template

register = template.Library()

@register.filter('modulo')
def modulo(value,divisor) : 

    return value%divisor
