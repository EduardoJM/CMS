from django import template
from blog.models import NavBarLink

register = template.Library()

@register.inclusion_tag('blog/parts/navbar_links.html', takes_context=True)
def navbar_links(context):
    return {
        'links': NavBarLink.objects.all(),
        'request': context['request'],
    }
