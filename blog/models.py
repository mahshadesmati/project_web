from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    STATUS = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="blog_posts")
    title = models.CharField(max_length=250)
    body = RichTextField()
    short_description = models.TextField(verbose_name="توضیح کوتاه", blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="published")
    publish = models.DateTimeField(default=timezone.now)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    views = models.PositiveIntegerField(default=0)
    cover = models.ImageField(upload_to='covers%Y%m%d', default="default-avatar.png")

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("publish",)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.ForeignKey(get_user_model() ,verbose_name=_("نویسنده"), max_length=50, on_delete=models.CASCADE)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("datetime_created", )

    def __str__(self):
        return f"comment by {self.name} on {self.post}"
