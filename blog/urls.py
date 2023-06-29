from django.urls import path

from .feeds import LatestPostFeed

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="home"),
    path("about/", views.about, name="about"),
    path("tag/<slug:tag_slug>", views.post_list, name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<int:pk>", views.post_detail, name="post_detail"),
    # path("<int:pk>/share/", views.share_post, name="share_post"),
    path("feed/", LatestPostFeed(), name="post_feed"),
    # path("search/", views.search_view, name="post_search"),
    path("create/", views.post_create, name="post_create"),
    path("<int:year>/<int:month>/<int:day>/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("<int:year>/<int:month>/<int:day>/<int:pk>/update/", views.PostUpdateView.as_view(), name="edit_post"),
]
