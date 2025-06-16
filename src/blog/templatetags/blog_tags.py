import math

from django import template

from blog.models import NavBarLink

register = template.Library()

@register.inclusion_tag('blog/parts/navbar_links.html', takes_context=True)
def navbar_links(context):
    queryset = NavBarLink.objects.select_related('page').all()
    return {
        'links': queryset.all(),
        'request': context['request'],
    }

@register.simple_tag
def tags_cloud_weight(num, data):
    if not data:
        return '1'
    max_num = 9
    max_found = 0
    for i in data:
        if i['num_posts'] > max_found:
            max_found = i['num_posts']
    
    if not max_found:
        return '1'

    factor = max_num / max_found

    return str(math.floor(num * factor))
