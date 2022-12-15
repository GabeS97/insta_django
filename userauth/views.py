from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from post.models import Post, Follow, Stream
from .models import Profile
# Create your views here.
def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-created_at')
    else:
        posts.favorite.all()

    # Tracking profile stats
    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    follower_count = Follow.objects.filter(following=user).count()

    # Follow status
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
    # Pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts_paginator': posts_paginator,
        'profile': profile,
        'posts': posts,
        'post_count': post_count,
        'following_count': following_count,
        'follower_count': follower_count,
        'follow_status': follow_status
    }

    return render(request, 'profile.html', context)

def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)
    try:
        print('\n\n', option, '\n\n')
        f, created = Follow.objects.get_or_create(follower=user, following=following)
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=user).all().delete()
        else:
            posts = Post.objects.filter(user=following)[:10]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.created_at, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))

def editProfile(request):
    user = request.user
    profile = Profile.objects.get(user__id=user)

    if request.method == 'POST':
        form = EditFormProfile(request.POST, request.FILES)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.bio = form.cleaned_data.get('bio')
            profile.url = form.cleaned_data.get('url')
            profile.save()
            return redirect('profile')
        else:
            form = EditFormProfile()
            context = {
                'form': form ,
            }
        return render(request, 'edit-profile.html', context)
