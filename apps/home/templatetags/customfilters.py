from django import template

register = template.Library()

@register.filter
def get_dictionary_value(item,tag):
    return item[tag]

@register.filter
def item_name(obj):
    return obj.model.objects.get(pk=obj.kwargs['pk'])