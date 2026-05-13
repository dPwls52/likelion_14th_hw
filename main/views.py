from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# Create your views here.

def mainpage(request):
    context = {
        'generation': 14,                   
        'info': {                           
            'projectapp': '프로젝트는 하나의 서비스 전체이고 앱은 프로젝트를 구성하는 기능들의 집합',
            'Django': '데이터를 정의하는 모델과 화면을 만드는 템플릿 사이에서 뷰가 사용자의 요청을 처리하고 결과를 전달해주는 방식',
        },
        
    }
    return render(request, 'main/mainpage.html', context)


def secondpage(request):
    context = {                         
        'info': {     
            'mbti': 'intp',                       
            
        },
        
    }
    return render(request, 'main/secondpage.html', context)    

def new_post(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'main/new_post.html')    

def create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    new_post = Post()

    new_post.title = request.POST['title']
    new_post.writer = request.user
    new_post.pub_date = request.POST['pub_date']
    new_post.content = request.POST['content']
    new_post.mood = request.POST['mood']

    new_post.save()
    save_tags(new_post)

    return redirect('main:detail', new_post.id)

def postpage(request):
    posts = Post.objects.all()
    return render(request, 'main/postpage.html', {'posts': posts})

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST' and request.user.is_authenticated:
        new_comments = Comment()

        new_comments.post = post
        new_comments.writer = request.user
        new_comments.content = request.POST['content']

        new_comments.save()
        return redirect('main:detail', post_id)

    comments = Comment.objects.filter(post=post)
    return render(request, 'main/detail.html', {'post': post, 'comments': comments})

def edit_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    comment_post = get_object_or_404(Comment, pk=comment_id)

    if comment_post.writer != request.user:
        return redirect('main:detail', comment_post.id)

    return render(request, 'main/edit_comment.html', {'comment': comment_post})


def edit(request, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    edit_post = get_object_or_404(Post, pk=post_id)

    if edit_post.writer != request.user:
        return redirect('main:detail', edit_post.id)

    return render(request, 'main/edit.html', {'post': edit_post})

def delete(request, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    delete_post = get_object_or_404(Post, pk=post_id)

    if delete_post.writer != request.user:
        return redirect('main:detail', delete_post.id)
        
    delete_post.delete()

    return redirect('main:postpage')

def update(request, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    update_post = get_object_or_404(Post, pk=post_id)

    if update_post.writer != request.user:
        return redirect('main:detail', update_post.id)

    update_post.title = request.POST['title']
    update_post.writer = request.user
    update_post.pub_date = request.POST['pub_date']
    update_post.content = request.POST['content']
    update_post.mood = request.POST['mood']    
    update_post.save()    

    save_tags(update_post)

    return redirect('main:detail', update_post.id)   

def update_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    update_c = get_object_or_404(Comment, pk=comment_id)

    if update_c.writer != request.user:
        return redirect('main:detail', update_c.post.id) 
    
    update_c.content = request.POST['content']
    update_c.save() 

    return redirect('main:detail', update_c.post.id)

def delete_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    delete_c = get_object_or_404(Comment, pk=comment_id)

    if delete_c.writer != request.user:
        return redirect('main:detail', delete_c.post.id)

    delete_c.delete()

    return redirect('main:detail', delete_c.post.id)

def save_tags(post):
    words = post.content.split()
    tag_list = []

    for w in words:
        if len(w) > 0:
            if w[0] == '#':
                tag_list.append(w[1:])

    post.tags.clear()

    for t in tag_list:
        tag, boolean = Tag.objects.get_or_create(name=t)
        post.tags.add(tag)

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'main/tag_list.html', {'tags': tags})

def tag_post_list(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    posts = tag.posts.all()
    return render(request, 'main/tag_post_list.html', {'tag': tag, 'posts': posts})

def likes(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user in post.like.all():
        post.like.remove(request.user)
        post.like_count -= 1
        post.save()
    else:
        post.like.add(request.user)
        post.like_count += 1
        post.save()
    return redirect('main:detail', post.id)

def comment_likes(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user in comment.like.all():
        comment.like.remove(request.user)
        comment.like_count -= 1
        comment.save()
    else:
        comment.like.add(request.user)
        comment.like_count += 1
        comment.save()
    return redirect('main:detail', comment.post.id)