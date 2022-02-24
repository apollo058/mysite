from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from ..models import Question

def index(request):
    '''
    mysite 목록 출력
    '''
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent') # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(subject__icontains=kw)

    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'mysite/question_list.html', context)

def detail(request, question_id):
    '''
    mysite 내용 출력
    '''
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'mysite/question_detail.html', context)