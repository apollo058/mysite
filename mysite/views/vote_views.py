from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, resolve_url

from ..models import Question, Answer

@login_required(login_url='common:login')
def vote_question(request, question_id):
    '''
    mysite 질문추천등록
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    elif question.voter.exists():
        question.voter.clear()
    else:
        question.voter.add(request.user)
    return redirect('mysite:detail', question_id=question.id)

@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    """
    mysite 답글추천등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    elif answer.voter.exists():
        answer.voter.clear()
    else:
        answer.voter.add(request.user)
    return redirect('mysite:detail', question_id=answer.question.id)