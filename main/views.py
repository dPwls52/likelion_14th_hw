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
    return render(request, 'main/new_post.html')    

def create(request):
    new_post = Post()

    new_post.title = request.POST['title']
    new_post.writer = request.POST['writer']
    new_post.pub_date = request.POST['pub_date']
    new_post.content = request.POST['content']
    new_post.mood = request.POST['mood']

    new_post.save()

    return redirect('main:detail', new_post.id)

def postpage(request):
    posts = Post.objects.all()
    return render(request, 'main/postpage.html', {'posts': posts})

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'main/detail.html', {'post': post})

def edit(request, post_id):
    edit_post = get_object_or_404(Post, pk=post_id)
    return render(request, 'main/edit.html', {'post': edit_post})

def delete(request, post_id):
    delete_post = get_object_or_404(Post, pk=post_id)
    delete_post.delete()

    return redirect('main:postpage')

def update(request, post_id):
    update_post = get_object_or_404(Post, pk=post_id)
    update_post.title = request.POST['title']
    update_post.writer = request.POST['writer']
    update_post.pub_date = request.POST['pub_date']
    update_post.content = request.POST['content']
    update_post.mood = request.POST['mood']    
    update_post.save()    

    return redirect('main:detail', update_post.id)   