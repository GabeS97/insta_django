from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tag, Stream, Follow, Post
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
