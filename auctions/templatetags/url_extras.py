from django import template
from django.utils.http import urlencode


register = template.Library()

@register.simple_tag(takes_context=True)
def query_params(context, **kwargs):
    # Get current URL query parameters
    d = context['request'].GET.copy()
    # Add key:value pairs from tag function call
    for k, v in kwargs.items():
        d[k] = v
    # Return encoded dictionary containing updated query params
    return d.urlencode()
