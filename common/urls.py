from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup')
]

"""
보통 app_name과 urlpatterns의 name이 연동된다고 생각하면 쉽다.
예를 들어 urls.py 파일 내에 app_name이 'common'이고, urlpatterns 리스트에 작성된 path의 name 값들이
각각 'login', 'logout', 'signup'이라고 할 때 이를 조합하면 아래와 같이 사용할 수 있게된다.

{% url 'common:login' %}
{% url 'common:logout' %}
{% url 'common:signup' %}

.html에 작성된 페이지에서 위 url을 호출하게되면 각각의 패턴에서 작성된 함수를 호출하게 된다. 
호출될 때의 방식이 GET이냐 POST이냐에 따른 함수 실행은 각각의 함수의 내용에서 작성하게 된다.

"""
