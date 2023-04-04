from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import (
    Post,
    Comment,
    Vote
)
from .forms import (
    UpdateCreatePostForm,
    CommentCreateForm,
    SearchForm,
)
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        if request.GET.get("search"):
            posts = posts.filter(body__contains=request.GET["search"])
        return render(request, 'home/index.html', {"posts": posts,
                                                   "form": self.form_class})


class PostDetailView(View):
    form_class = CommentCreateForm
    post_obj = None

    def setup(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, id=kwargs["post_id"],
                                          slug=kwargs["post_slug"])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_obj.p_comments.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_obj.user_can_like(
                request.user):
            can_like = True
        return render(request, 'home/detail.html', {"post": self.post_obj,
                                                    "comments": comments,
                                                    "form": self.form_class,
                                                    "can_like": can_like})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_obj
            new_comment.save()
            messages.success(request, "create was successfully", 'success')
            return redirect('home:detail', self.post_obj.id, self.post_obj.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "delete was successfully", 'success')
        else:
            messages.error(request, "you can't delete this post", 'danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = UpdateCreatePostForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, id=kwargs["post_id"])
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
            return redirect('home:detail', kwargs["post_id"],
                            self.post_instance.slug)


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


class ReplyCommentView(View):
    form_class = CommentCreateForm

    def post(self, request, post_id, comment_id):
        post_o = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post_o
            reply.is_reply = True
            reply.reply = comment
            reply.save()
            messages.success(request, "your reply successfully submit",
                             'success')
        return redirect('home:detail', post_id, post_o.slug)


class VoteCreateView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        post_o = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post_o, user=request.user)
        if like.exists():
            messages.error(request, "you have already this post", 'warning')
        else:
            Vote.objects.create(post=post_o, user=request.user)
            messages.success(request, "create was successfully", 'success')
        return redirect('home:detail', post_id, post_o.slug)
