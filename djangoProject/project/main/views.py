import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.crawling import crawling
# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from main.models import User_Info
from main.models import Course
from django.contrib.auth.models import User
from django.contrib import auth
from main.logic import scoreSum

# c1 = Course(course_name="빅데이터 서비스 분석 개발 6회차")
# c2 = Course(course_name="빅데이터 서비스 분석 개발 6회차")
# c3 = Course(course_name="빅데이터 서비스 분석 개발 6회차")
# c4 = Course(course_name="AI 개발 6회차")
# c5 = Course(course_name="AI 개발 6회차")
# c6 = Course(course_name="AI 개발 6회차")
# c7 = Course(course_name="클라우드 서비스 개발 6회차")
# c8 = Course(course_name="클라우드 서비스 개발 6회차")
# c9 = Course(course_name="클라우드 서비스 개발 6회차")
# c10 = Course(course_name="빅데이터 서비스 분석 개발 6회차")
# c11 = Course(course_name="빅데이터 서비스 분석 개발 6회차")
# c12 = Course(course_name="빅데이터 서비스 분석 개발 6회차")
#
# c1.save(); c2.save(); c3.save();
# c4.save(); c5.save(); c6.save();
# c7.save(); c8.save(); c9.save();
# c10.save(); c11.save(); c12.save();
#
# u1 = User(password="1",username="e",first_name="조원형")
# u2 = User(password="2",username="f",first_name="이찬영")
# u3 = User(password="3",username="g",first_name="박정수")
# u4 = User(password="4",username="h",first_name="윤동열")
# u5 = User(password="5",username="j",first_name="김종태")
# u6 = User(password="4",username="k",first_name="이동훈")
# u7 = User(password="5",username="m",first_name="표영우")
# u8 = User(password="4",username="t",first_name="김용록")
# u9 = User(password="6",username="z",first_name="나나나")
# u10 = User(password="6",username="L",first_name="노노")
# u11 = User(password="6",username="K",first_name="누누")
# u12 = User(password="8",username="S",first_name="니니")
# u1.save(); u2.save(); u3.save();
# u4.save(); u5.save(); u6.save();
# u7.save(); u8.save(); u9.save();
# u10.save(); u11.save(); u12.save();
#
# u_info1 = User_Info(user=u1,score=10.0,course=c1)
# u_info2 = User_Info(user=u2,score=5.0,course=c2)
# u_info3 = User_Info(user=u3,score=7.0,course=c3)
# u_info4 = User_Info(user=u4,score=7.0,course=c4)
# u_info5 = User_Info(user=u5,score=8.0,course=c5)
# u_info6 = User_Info(user=u6,score=9.0,course=c6)
# u_info7 = User_Info(user=u7,score=11.0,course=c7)
# u_info8 = User_Info(user=u8,score=4.0,course=c8)
# u_info9 = User_Info(user=u9,score=11.0,course=c9)
# u_info10 = User_Info(user=u10,score=12.0,course=c10)
# u_info11 = User_Info(user=u11,score=13.0,course=c11)
# u_info12 = User_Info(user=u12,score=15.0,course=c12)
# u_info1.save(); u_info2.save(); u_info3.save()
# u_info4.save(); u_info5.save(); u_info6.save()
# u_info7.save(); u_info8.save(); u_info9.save()
# u_info10.save(); u_info11.save(); u_info12.save()

#crawling_tmp = crawling()

def homeView(request):
    # context = {
    #      'images': crawling_tmp[0],
    #      'urls': crawling_tmp[1],
    #      'status': crawling_tmp[2],
    #      'n': range(len(crawling_tmp[0])),
    #  }
    return render(request, 'home.html', None)

def teamView(request):
    return render(request,'team.html',None)

def teamRefresh(request, idx):
    return render(request,)

def teamJson(request):

    # 과정명 가져오기
    jsonObject = json.loads(request.body)
    course = jsonObject.get('course')
    # 해당 과정명에 해당하는 모든 인원 뽑아오기
    objs = list(Course.objects.filter(course_name=course))
    names = []
    for obj in objs:
        id = obj.id
        user_info = User_Info.objects.get(course_id=id)
        names.append(user_info.user.first_name)

    context = {
        'names': names,
        'course': course,
    }
    return JsonResponse(context)

def teamJson2(request):
    pass

def joinView(request):
    return render(request, 'join.html', None)

def editView(request):
    return render(request,'edit.html',None)

def loginView(request):
    return render(request,'login.html',None)

def qnaView(request):
    return render(request,'qna.html',None)

def qnaWriteView(request):
    return render(request,'qnaWrite.html',None)

def guideView(request):
    return render(request,'guide.html',None)

