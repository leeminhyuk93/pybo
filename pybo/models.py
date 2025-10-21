from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# 질문 모델 클래스
class Question(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    votor = models.ManyToManyField(User, related_name='votor_question')
    
    def __str__(self):
        return self.subject
    
# 대답 모델 클래스
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # 외래키지정, 삭제옵션은 연결 모델의 데이터 삭제 시 동일하게 삭제
    content = models.TextField(
        validators=[
            MinLengthValidator(5, '답변은 최소 5자 이상 입력해야 합니다.')
        ]
    )
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    votor = models.ManyToManyField(User, related_name='votor_answer')
    
    def __str__(self):
        return self.content
    
    