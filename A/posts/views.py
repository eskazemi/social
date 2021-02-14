from django.shortcuts import render,get_object_or_404,redirect
from .forms import AddPostForm,EditPostForm,AddCommentForm,AddReplyForm
from .models import Post,Comment
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

def all_posts(request):
    posts=Post.objects.all()
    return render(request,'posts/all_posts.html',{'posts':posts})
def detail_post(request,year,month,day,slug):
    post=get_object_or_404(Post, create__year=year,create__month=month,
    create__day=day,slug=slug)
    comments=Comment.objects.filter(post=post,is_reply=False)
    reply_form=AddReplyForm()
    if request.method=='POST':
        form=AddCommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.user=request.user
            new_comment.save()
            messages.success(request,'publish comment successfully','success')

    else:
        form=AddCommentForm()
    return render(request,'posts/detail_post.html',{'post':post,'comments':comments,'form':form,'reply':reply_form})

@login_required
def add_post(request,user_id):
    if request.user.id==user_id:
        if request.method=="POST":
            form=AddPostForm(request.POST)
            if form.is_valid():
                new_post=form.save(commit=False)
                new_post.user=request.user
                new_post.slug=slugify(form.cleaned_data['body'][:30],allow_unicode=True)
                new_post.save()
                messages.success(request,'this is post publish successfully','success')
                return redirect('account:user_dashboard',user_id)

        else:
            form=AddPostForm()
        return render(request,'posts/add_post.html',{'form':form})
    else:
        return redirect('posts:all_posts')

@login_required
def post_delete(request,user_id,post_id):
    if request.user.id == user_id:
        Post.objects.filter(pk=post_id).delete()
        messages.success(request,'your post delete successfully','success')
        return redirect('account:user_dashboard',user_id)
    else:
        return redirect('posts:all_posts')
@login_required
def post_edit(request,user_id,post_id):
    post=get_object_or_404(Post,pk=post_id)
    if request.user.id ==  user_id:
        if request.method=='POST':
            form=EditPostForm(request.POST,instance=post)
            if form.is_valid():
                ep=form.save(commit=False)
                ep.slug=slugify(form.cleaned_data['body'][:30],allow_unicode=True)
                form.save()
                messages.success(request,'edit post successfully','success')
                return redirect('account:user_dashboard',user_id)
        
        else:
            form=EditPostForm(instance=post)
        return render(request,'posts/edit_post.html',{'form':form})
    
    else:
        return redirect('account:user_dashboard',user_id)

@login_required
def add_reply(request,post_id,comment_id):
    post=get_object_or_404(Post , id=post_id)
    comment=get_object_or_404(Comment , pk=comment_id)
    if request.method=='POST':
        form=AddReplyForm(request.POST)
        if form.is_valid():
            reply=form.save(commit=False)
            reply.user=request.user
            reply.post=post
            reply.reply=comment
            reply.is_reply=True
            reply.save()
            messages.success(request,'reply successfully','success')
    return redirect ('posts:detail_post' ,post.create.year, post.create.month, post.create.day , post.slug)
        
    

