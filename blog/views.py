from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.decorators import login_required

from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm, PostCreateForm


def post_list(request, tag_slug=None):
    form = SearchForm()
    search = None
    posts = None
    count = 0
    tag = None
    page = None
    if "search" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data["search"]
            # A B C D -> 1 , 0.4 , 0.2 , 0.1
            search_vector = SearchVector("title", weight="A") + SearchVector("body", weight="B") + SearchVector("short_description", weight="B")
            search_query = SearchQuery(search)
            search_rank = SearchRank(search_vector, search_query)
            posts = Post.published.annotate(search=search_vector, rank=search_rank).filter(rank__gte=0.3).order_by("-rank")
    if not posts:
        posts = Post.published.all()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    if posts:
        count = posts.count()

        paginator = Paginator(posts, 6)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

    context = {"posts": posts, "page": page, "tag": tag, "form": form, "search": search, "count": count}
    return render(request, "blog/post_list.html", context)


# class PostListView(generic.ListView):
#     queryset = Post.published.all()
#     context_object_name = "posts"
#     template_name = "blog/post_list.html"
#     paginate_by = 3


def post_detail(request, year, month, day, pk):
    post = get_object_or_404(Post, pk=pk, status="published", publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish")[:3]

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_form = comment_form.save(commit=False)
            new_form.post = post
            new_form.name = request.user
            new_form.save()
            return redirect(request.path_info)
    else:
        comment_form = CommentForm()

    context = {
        "post": post,
        "form": comment_form,
        "comments": comments,
        "s_posts": similar_posts,
    }
    return render(request, "blog/post_detail.html", context)


@login_required()
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            tags = form.cleaned_data['tags']
            post.save()
            post.tags.add(*tags)
            return redirect("blog:home")
    else:
        form = PostCreateForm()

    return render(request, "blog/post_create.html", {"form": form})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("blog:home")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


# def update_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = PostCreateForm(request.POST or None, instance=post)
#     if form.is_valid():
#         form.save()
#         return redirect("posts")
#     else:
#         form = PostCreateForm(instance=post)
#
#     return render(request, "blog/edit_post.html", context={"form": form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostCreateForm

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


def about(request):
    return render(request, "blog/about.html")
