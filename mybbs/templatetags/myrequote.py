from django import template
register = template.Library()


@register.filter(name='myrequote')
def myrequote(value):
    value=value.replace('[quote]','<div style="padding:4px;background-color:#ffffe1;border:1px solid gray">')
    value=value.replace('[/quote]','</div>')
    return (value)

