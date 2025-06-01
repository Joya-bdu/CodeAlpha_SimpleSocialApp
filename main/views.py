from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import RegisterForm, PostForm, CommentForm
from django.contrib import messages
from .models import Post
from django.http import HttpResponseForbidden

def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'main/login.html') 

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main/home.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        Post.objects.create(author=request.user, content=content, image=image)
        return redirect('home')
    return render(request, 'main/post_create.html')
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    profile = post.author.profile

    # Check if current user liked this post
    user_liked = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'main/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'profile': profile,
        'user_liked': user_liked  # এখানে পাঠালাম
    })


@login_required
def profile_view(request, user_id=None):  # user_id optional
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user
    profile = user.profile

    if request.method == 'POST' and request.user == user:
        bio = request.POST.get('bio')
        profile.bio = bio
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        return redirect('my_profile') if not user_id else redirect('profile', user_id=user.id)

    return render(request, 'main/profile.html', {'profile': profile})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'main/post_list.html', {'posts': posts})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # চেক করো ইউজার আগে লাইক করেছে কি না
    like = Like.objects.filter(post=post, user=request.user).first()
    
    if like:
        # আগে লাইক করলে সেটা মুছে দাও (Unlike)
        like.delete()
    else:
        # নতুন লাইক তৈরি করো
        Like.objects.create(post=post, user=request.user)
    
    return redirect('post_detail', pk=post_id)

@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    profile = target_user.profile
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
    return redirect('profile', user_id=user_id)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        # অন্য কেউ ডিলিট করতে পারবে না
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('home')  # অথবা তোমার হোম পেইজের URL নাম

    # GET হলে কনফার্মেশন পেজ দেখাবে
    return render(request, 'main/post_confirm_delete.html', {'post': post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'main/post_edit.html', {'form': form, 'post': post})