from django import template
from forum.models import Topic
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('forum/topics_list.html')
def show_topics():
    topics = Topic.objects.annotate(cnt=Count('comment'))#.filter(cnt__gt=0)
    return {"topics": topics, }
