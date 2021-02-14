from django.shortcuts import render,redirect,get_object_or_404
from .form  import UserLoginForm,RegisterForm,EditProfileForm,PhoneLoginForm,VerifycodeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.decorators import login_required
from kavenegar import * 
from random import randint
from .models import Profile,Relation

def user_login(request):
    next=request.GET.get('next')
    if request.method =="POST":
        form=UserLoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request, username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,' you login successfully','success')
                if next:
                     return redirect(next)
                return redirect('posts:all_posts')
            else:
                messages.error(request,'wrong username or password','warning')

    else:
        form=UserLoginForm()
    return render(request,'account/login.html',{'form':form})

def RegisterUser(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=User.objects.create_user(cd['username'],cd['Email'],cd['password'])
            login(request,user)
            messages.success(request,'you register successfully ','success')
            return redirect('posts:all_posts')
    else:
        form=RegisterForm()
    return render(request,'account/Register.html',{'form':form})
    


@login_required
def user_logout(request):
    logout(request)
    messages.success(request,' you logout successfully','success')
    return redirect('posts:all_posts')

@login_required
def user_dashboard(request,user_id):
    user=get_object_or_404(User,pk=user_id)
    posts=Post.objects.filter(user=user)
    self_dash=False
    is_following=False
    relation=Relation.objects.filter(from_user=request.user,to_user=user)
    if relation.exists():
        is_following=True
    if request.user.id==user_id:
        self_dash=True
    return render(request,'account/dashboard.html',{'user':user,'posts':posts,'self_dash':self_dash,'is_following':is_following})


@login_required
def edit_profile(request,user_id):
    user=get_object_or_404(User,pk=user_id)
    if request.method =="POST":
        form=EditProfileForm(request.POST,instance=user.profile)
        if form.is_valid():
            form.save()
            user.email=form.cleaned_data['email']
            user.save()
            messages.success(request,'edit profile successfully','success')
        return redirect('account:user_dashboard',user_id)
    else:
        form=EditProfileForm(instance=user.profile,initial={'email':request.user.email,})
    return render (request,'account/edit_profile.html',{'form':form})

def phone_login(request):
    if request.method=="POST":
        form=PhoneLoginForm(request.POST)
        if form.is_valid():
            phone=f"0{form.cleaned_data['phone']}"
            rand_num=randint(1000,9999)
            api = KavenegarAPI('54325078707872505A6A654168745145656B39335544484A55774670715947666846616C3730636E6F796B3D')
            params = { 'sender' : '', 'receptor':phone, 'message' :rand_num} 
            response = api.sms_send( params) 
        return redirect('account:verify',phone,rand_num)
    else:
        form=PhoneLoginForm()
    return render(request,'account/phoneLogin.html',{'form':form})


def verify(request,phone,rand_num):
    if request.method=="POST":
        form=VerifycodeForm(request.POST)
        if form.is_valid():
            if rand_num==form.cleaned_data['code']:
                profile=get_object_or_404(Profile,phone=phone)
                user=get_object_or_404(User,profile__id=profile.id)
                login(request,user)
                messages.success(request,'your login successfully','success')
            return redirect('posts:all_posts')
    else:
        form=VerifycodeForm()
    return render(request,'account/verify.html',{'form':form})

def follow(request):
    pass

def unfollow(request):
    pass