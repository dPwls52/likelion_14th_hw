from django.shortcuts import render

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