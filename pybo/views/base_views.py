from django.shortcuts import render
from django.core.paginator import Paginator
from ..models import Question
from django.db.models import Q


# Create your views here.
def index(request):
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
        
    paginator = Paginator(question_list, 10) # question_list의 데이터를 10개씩 기준으로 나눔
    page_obj = paginator.get_page(page)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    # custum page data
    start_page = (page - 1) // 5 * 5 + 1
    end_page = min(start_page + 4, paginator.num_pages)
    current_block = (page - 1) // 5
    start_block = 0
    last_block = (paginator.num_pages - 1) // 5
    paging_data = {
        'current_page': page,
        'start_page_number': start_page,
        'end_page_number': end_page,
        'page_range': range(start_page, end_page + 1),
        'has_previous_block': start_block < current_block,
        'previous_block_start': max(start_page - 5, 0),
        'has_next_block': current_block < last_block,
        'next_block_start': start_page + 5,
    }
    
    context = {
        'question_list': page_obj,
        'paging_data': paging_data,
        'kw': kw,
    }
    return render(request, 'pybo/question_list.html', context)