from django import template

register = template.Library()


@register.filter
def getitem(value, index):
	return value[index]
