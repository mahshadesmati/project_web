from django import forms

from taggit.forms import TagField

from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    tags = TagField()


    class Meta:
        model = Post
        fields = ["title", "short_description", "body", "cover", "tags"]
        labels = {
            "title": "عنوان",
            "short_description": "توضیح کوناه",
            "body": "توضیحات",
            "cover": "تصویر",
        }



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20)
