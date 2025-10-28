from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# """
# 유저 회원가입 시 활용하는 폼.
# 원래 기본은 'UserCreationForm' 이다. 하지만 이메일 정보를 추가하기 위해서
# 해당 클래스를 상속시킨 후 email 항목을 추가했다. 
# """
class UserForm(UserCreationForm):
    """
    이메일 항목의 변수명은 email, 항목이름은 이메일로 설정.
    validators 에는 검증에 관련된 클래스를 입력할 수 있다.
    여기서는 EmailValidator 한 가지만 추가하였다.
    """
    email = forms.EmailField(label="이메일", validators=[
        EmailValidator() # 이메일 검증 클래스
    ])
    
    """
    모델 폼을 작성할 때는 항상 'Meta' 클래스를 필수로 작성하여야한다.
    메타클래스에는 현재 어떤 객체를 대상으로 폼을 작성하는지, 필드는 무엇이 있는지
    내용을 사전에 작성한다.
    *
      예상으로는 필드의 이름을 작성함으로써 직접 변경이 가능한 항목을 제한할 수 있을 것이다.
      그렇게 하나의 객체를 대상으로 여러가지 폼을 작성할 수 있을 것이다.
      예를 들면 학생의 데이터를 관리하는 폼이 있는데 수학선생님은 수학에 관련된 것만,
      영어선생님은 영어에 관련된 데이터만 수정할 수 있도록 하는 것이다. 
    *
    """
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
        