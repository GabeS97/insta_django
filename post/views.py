from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from userauth.models import Profile
from .models import Tag, Stream, Follow, Post, Like
from .forms import NewPostForm
# Create your views here.
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-created_at')
    context = {
        'post_items': post_items
    }
    return render(request, 'index.html', context)

def newPost(request):
    user = request.user.id
    tags_objs =[]

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tag')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p, created = Post.objects.get_or_create(image=image, caption=caption, user_id=user)
            p.tag.set(tags_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()
    context = {
        'form': form
    }
    return render(request, 'createpost.html', context)

def postDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'post-details.html', context)

def tags(reqest, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.fitler(tag-tag).order_by('-created_at')

    context = {
        'tags': tag,
        'posts': posts
    }

    return render(request, 'tags.html', context)

def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Like.objects.filter(user=user, post=post).count()

    if not liked:
        liked = Like.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = Like.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('post-details', args=[post_id]))

def favorite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    if profile.favorite.filter(id=post_id).exists():
        profile.favorite.remove(post)
    else:
        profile.favorite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))
