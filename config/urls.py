"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

"""
'admin/'은 기본설정으로 해당 url로 접속하면 관리대상의 데이터베이스(모델, 유저 등)를 조작할 수 있다.
해당 주소에서는 관리자로 설정된 슈퍼유저만 로그인이 가능하다.

두 번째 path에서는 ''('/') 기본 접속주소를 입력하면 리다이렉트로 다른 주소의 url을 요청할 수 있게 하는 
코드이다. 주의할 점은 include랑 병행해서 사용하면 안된다는 것이다.  RedirectView의 as_view의 url인자로
패턴 주소를 입력하면 해당 패턴으로 재실행하게 된다. 아래 코드에서는 ''로 접속을 시도하면 '/pybo/question_list'를 요청한다.
그럼 아래의 'pybo/question_list/'와 매칭된다. 두 번째 인자로 parmanent 값이 False로 되어 있는데 이 접속을
브라우저 캐시로 등록하지 않겠다는것이다.(캐시로 등록하지 않으면 자동완성이 되지 않음)
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/pybo/question_list', permanent=False)), # 기본 url 입력 시 /pybo/로 리다이렉트
    path('pybo/question_list/', include('pybo.urls')),
    path('common/', include('common.urls')),
]
