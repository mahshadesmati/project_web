from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "status", "publish"]
    list_filter = ["status"]
    search_fields = ["title", "body"]
    date_hierarchy = "publish"
    list_editable = ["status"]



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "active", "datetime_created"]
    list_filter = ["active"]
    search_fields = ["name", "body"]
    list_editable = ["active"]
