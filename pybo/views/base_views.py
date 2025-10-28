from django.shortcuts import render
from django.core.paginator import Paginator
from ..models import Question
from django.db.models import Q


# Create your views here.
"""
index를 호출하면 page, kw 값을 받아서 검색될 리스트를 Paginator 객체로 변환하여 
렌더링될 페이지와 함께 전달한다.
"""
def index(request):
    """
    요청 객체에서 GET(url주소에 입력된)데이터 page(페이지), kw(검색키워드)를 가져온다.
    쓰임새는 kw로 검색하여 일치하는 내용의 page번째의 데이터를 보여주도록 한다.
    """
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    
    
    """
    question_list에는 Question 모델데이터가 가지고 있는 내용을 -create_date(작성일자 거꾸로)옵션으로 
    정렬하여 가져온 것이다. 
    만약 GET 데이터에 kw 값이 존재하면 해당 키워드를 사용하여 question_list를 가져온다.
    
    여기에서 Q는 부분적으로 일치하는 데이터를 가져오기 위해 사용한다.
    'subject__icontains=kw'는 현재 객체의 필드인 subject의 문자열 중에서 kw가 부분적으로 포함하는지를
    말한다. | (or)연산을 통해서 총 5개의 부분적으로 일치하는 데이터를 가져온다.
    여기에서 icontains는 대소문자 관계없이 일치하는지를 말하고 여기에서 i를 제외하면 대소문자도 정확히 일치하는지
    를 기준으로 판단하게 된다.
    
    제목__icontains=kw
    내용__icontains=kw
    대답__내용__icontains=kw
    작성유저__유저이름__icontains=kw
    대답__작성유저__유저이름__icontains=kw
    
    그리고 마지막으로 이 필터된 데이터에서 .distinct()를 호출한다. 이는 중복을 제거하고 반환하는 함수이다.
    """
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    
    """
    Paginator 클래스는 question_list의 내용을 10개를 하나의 페이지로 하여 구분한다.
    Paginator 인스턴스로 get_page() 함수를 호출하면 page 숫자에 해당하는 데이터들을 가져온다.
    """    
    paginator = Paginator(question_list, 10) # question_list의 데이터를 10개씩 기준으로 나눔
    page_obj = paginator.get_page(page)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    """
    아래는 현재 페이지가 주어졌을 때 하단에 표시되는 페이지 수를 조정하기 위한 데이터들이다.
    
    start_page에 계산된 값은 현재 페이지가 만일 7이라하고, 총 5개의 페이지만 표시한다고 생각해보자
    그럼 페이지 7이 포함된 블록의 페이지는 6, 7, 8, 9, 10 일 것이다. 
    
    우선 index 값을 계산하기 위해 시작 값을 1이 아닌 0으로 만들어야 하기 때문에 
    '현재 페이지 - 1'을 계산해준다. 그렇게 나온 값 6을 다시 '6 // 5'를 계산하여 나온 값의
    몫만 사용하도록한다. 그렇게하면 현재의 페이지가 몇 번째 블록에 포함되는지가 계산된다. 
    6 // 5의 값을 1이므로 블록의 인덱스도 0부터 시작한다고 가정하면 1은 두번째 블록이다. 
    블록의 시작 페이지 값을 계산하기 위해 표시될 페이지 수인 5를 곱한다. 
    두 번째 블록이면 5, 세 번째 블록이면 10이 된다. 이는 이전 블록의 마지막 페이지 이므로 1을 더해서
    현재 블록의 시작 값으로 만든다.
    
    end_page는 마지막에 표시될 숫자로 start_page에서 4를 더하면 된다. 하지만 +4를 더한 페이지 수가 마지막
    페이지보다 클 가능성이 있기 때문에 마지막 페이지로 길이를 제한한다.
    
    current_block 현재 블록을 나타낸다.
    
    start_block, last_block은 페이지를 처음 또는 마지막으로 이동할 때 현재 블록이 처음 또는 마지막인 
    경우를 비교하기 위해서 작성하였다.
    
    has_previous_block, has_next_block은 다음 또는 이전 버튼을 눌렀을 때 이동할 블럭이 존재하는지를 
    확인할 때 사용한다.
    
    previous_block_start, next_block_start는 다음 또는 이전 버튼으로 이동할 때 적용할 페이지를 나타낸다.
    """
    # custum page data
    start_page = (page - 1) // 5 * 5 + 1
    end_page = min(start_page + 4, paginator.num_pages)
    current_block = (page - 1) // 5
    start_block = 0
    last_block = (paginator.num_pages - 1) // 5
    paging_data = {
        'current_page': page,                               # 현재 페이지
        'start_page_number': start_page,                    # 블록의 시작 번호
        'end_page_number': end_page,                        # 블록의 끝 번호
        'page_range': range(start_page, end_page + 1),      # 블록의 시작 번호 ~ 끝 번호 범위
        'has_previous_block': start_block < current_block,  # 이전 블록 존재 유무
        'previous_block_start': max(start_page - 5, 0),     # 이전 블록 시작 숫자
        'has_next_block': current_block < last_block,       # 다음 블록 존재 유무
        'next_block_start': start_page + 5,                 # 다음 블록 시작 숫자
    }
    
    """
    여기에서 kw를 전달해야 검색을 실행할 때 사라지지 않고 그대로 유지된다.
    """
    context = {
        'question_list': page_obj,
        'paging_data': paging_data,
        'kw': kw,
    }
    return render(request, 'pybo/question_list.html', context)