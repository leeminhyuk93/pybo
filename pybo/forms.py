from django import forms
from pybo.models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = {'subject', 'content'}
        labels = {
            'subject': '제목',
            'content': '질문내용'
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = {'content'}
        labels = {
            'content': '답변내용'
        }