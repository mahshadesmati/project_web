from django import template
from django.utils.safestring import mark_safe
import markdown

from blog.models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/post_delete.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"ssss ": latest_posts}


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter
def removewhitespace(text):
    value = ""
    for i in text:
        value += str(i)+", "
    value = value.replace('\n', '')
    value = value.replace('\r', '')
    value = value.replace(' ', '')
    return value
