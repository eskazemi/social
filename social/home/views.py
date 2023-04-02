from django.shortcuts import (
    render,
    redirect,
)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Post
from .forms import UpdateCreatePostForm
from django.utils.text import slugify


class HomeView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {"posts": posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug, *args, **kwargs):
        post = Post.objects.get(id=post_id, slug=post_slug)
        return render(request, 'home/detail.html', {"post": post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id, *args, **kwargs):
        post = Post.objects.get(id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "delete was successfully", 'success')
        else:
            messages.error(request, "you can't delete this post", 'danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = UpdateCreatePostForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(id=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):

        if self.post_instance.user.id != request.user.id:
            messages.error(request, "you can't update this post", 'danger')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.post_instance)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.post_instance)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, "update was successfully", 'success')
            return redirect('home:detail', kwargs["post_id"], self.post_instance.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = UpdateCreatePostForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, "create was successfully", 'success')
            return redirect('home:detail', new_post.id, new_post.slug)
