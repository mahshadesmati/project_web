from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


from .models import CustomUser
from .forms import UserForm


class UserUpdate(generic.UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("blog:home")
