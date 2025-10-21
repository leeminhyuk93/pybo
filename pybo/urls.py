from django.urls import path
from .views import base_views, question_views, answer_views

app_name = 'pybo'

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),
    
    # question_views.py
    path('question/create', question_views.question_form, name='question_form'),
    path('question/<int:question_id>', question_views.detail, name='detail'),
    path('question/modify/<int:question_id>', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>', question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>', question_views.question_vote, name='question_vote'),
    
    # answer_views.py
    path('answer/create/<int:question_id>', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>', answer_views.answer_delete, name='answer_delete'),
]
