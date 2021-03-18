from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Info, Answer
from django.utils import timezone
from .forms import InfoForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse
from main.resources import InfoResource
import csv

@login_required(login_url='common:login')
@permission_required('main.view_info', login_url='common:login', raise_exception=False)
def index(request):
    """
    목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'popular':
        info_list = Info.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    elif so == 'me':
        info_list = Info.objects.annotate(num_answer=Count('answer')).filter(num_answer=0).order_by('-create_date')
    else:  # recent
        info_list = Info.objects.order_by('-create_date')

    # 조회
    if kw:
        info_list = info_list.filter(
            Q(name__icontains=kw) |  # 이름검색
            Q(message__icontains=kw) |  # 내용검색
            Q(answer__author__username__icontains=kw) | # 답변 글쓴이검색
            Q(answer__memo__icontains=kw) # 메모검색
        ).distinct()
    # 페이징처리
    paginator = Paginator(info_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'info_list': page_obj, 'page': page, 'kw': kw, 'so': so}  # page, kw, so가 추가되었다.
    return render(request, 'main/info_list.html', context)

@login_required(login_url='common:login')
@permission_required('main.view_info', login_url='common:login', raise_exception=False)
def detail(request, info_id):
    """
    상담 내용 출력
    """
    info = get_object_or_404(Info, pk=info_id)
    context = {'info': info}
    return render(request, 'main/info_detail.html', context)

@login_required(login_url='common:login')
@permission_required('main.view_info', login_url='common:login', raise_exception=False)
def answer_create(request, info_id):
    """
    메모등록
    """
    info = get_object_or_404(Info, pk=info_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.info = info
            answer.save()
            return redirect('main:detail', info_id=info.id)
    else:
        form = AnswerForm()
    context = {'info': info, 'form': form}
    return render(request, 'main/info_detail.html', context)

def info_create(request):
    """
    정보입력
    """
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.create_date = timezone.now()
            info.save()
            messages.success(request, '제출해 주셔서 감사합니다!')
            return redirect('main:info_create')
    else:
        form = InfoForm()
    context = {'form': form}
    return render(request, 'main/info_form.html', context)

@login_required(login_url='common:login')
@permission_required('main.view_info', login_url='common:login', raise_exception=False)
def answer_modify(request, answer_id):
    """
    메모수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('main:detail', info_id=answer.info.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now() #수정일시 저장
            answer.save()
            return redirect('main:detail', info_id=answer.info.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'main/answer_form.html', context)

@login_required(login_url='common:login')
@permission_required('main.view_info', login_url='common:login', raise_exception=False)
def answer_delete(request, answer_id):
    """
    메모삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('main:detail', info_id=answer.info.id)

def export(request):
    info_resource = InfoResource()
    dataset = info_resource.export()
    # r2 = Info.objects.all()
    # info_resource = r2[0].answer_set.all()
    response = HttpResponse(dataset.xls, content_type='text/xls')
    response['Content-Disposition'] = 'attachment; filename="info.xls"'
    # writer = csv.writer(response)
    # writer.writerow(['Name', 'Ph', 'Message', 'Create_date', 'Agree'])
    #
    # r2 = Info.objects.all()
    # # r1 = r2[0].answer_set.all()
    # for ld in r2:
    #     writer.writerow(r2)
    return response
