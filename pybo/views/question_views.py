from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Question
from ..forms import QuestionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json


@login_required(login_url='common:login')
def question_form(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    """
    아래 코드는 객체가 없을 때 404 페이지 없음을 표시하지 않고, 
    사용자에게 얼럿창을 표시하고 다시 메인 페이지로 돌아가는 방법
    """
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     return HttpResponse("""
    #         <script>
    #             alert("페이지가 존재하지 않습니다.");
    #             window.location.href = "/";
    #         </script>                    
    #     """)
    votors = list(question.votor.values("id", "username"))
    context = {
        'question': question,
        'votors_json': json.dumps(votors),
    }
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question) # intance를 question으로 설정하면 question의 내용이 폼의 값에 할당된다.
        
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')
    
@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        if request.user in question.votor.all():
            question.votor.remove(request.user)
        else:
            question.votor.add(request.user)
    return redirect('pybo:detail', question_id=question.id)