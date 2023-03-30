from django.shortcuts import render
from django.views import View
from .models import Post


class HomeView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {"posts": posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug, *args, **kwargs):
        post = Post.objects.get(id=post_id, slug=post_slug)
        return render(request, 'home/detail.html', {"post": post})
