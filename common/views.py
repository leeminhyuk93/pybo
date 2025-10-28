from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from common.forms import UserForm

# Create your views here.
"""
logout_view 함수를 호출하면 request에 존재하는 유저의 로그아웃과 관련된 내용을
실행한 후 기본 페이지 '/'로 리다이렉트한다.
"""
def logout_view(request):
    logout(request)
    return redirect('/')


"""
signup 함수를 호출하면 request(요청)의 방식이 POST로 호출되었을 때 폼에 입력된 값들을 가지고 
회원가입 기능을 실행한다.
"""
def signup(request):
    # 현재 요청이 POST 요청일 때
    if request.method == "POST":
        # UserForm의 인자로 요청 객체의 POST 데이터를 입력
        form = UserForm(request.POST) 
        # 폼의 요청에 오류가 없는 경우
        if form.is_valid():
            # 폼의 내용을 데이터베이스에 바로 저장한다.
            # * commit=False 설정을 할 경우 폼의 데이터만 반환 *
            form.save()
            # 폼의 데이터 중 'username'
            username = form.cleaned_data.get('username')
            # 폼의 데이터 중 'password1'
            raw_password = form.cleaned_data.get('password1')
            
            ## 폼에 입력된 내용을 데이터베이스에 등록함과 동시에 로그인을 진행
            # 인증에 성공하면 유저 객체를 반환함
            user = authenticate(username=username, password=raw_password)
            # 현재 요청객체와 유저에 대한 객체를 전달하여 로그인 수행
            login(request, user)
            # 로그인 후 '/'으로 리다이렉트
            return redirect('/')
    else:
        # signup 요청이 GET 방식으로 전달된 경우 회원가입양식을 작성하는 화면으로 넘어감
        form = UserForm()
    # common/signup.html 페이지로 폼객체와 함께 렌더링
    return render(request, 'common/signup.html', {'form': form})