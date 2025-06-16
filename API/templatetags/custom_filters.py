from django import template

register = template.Library()

@register.filter
def dict_key(diccionario, clave):
    return diccionario.get(clave, False)


   
