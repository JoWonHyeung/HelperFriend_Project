import json
import os.path

from main.crawling import crawling
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from main.models import User_Info, UploadFile
from main.models import Course
from django.contrib.auth.models import User
from django.contrib import auth
from main.logic import scoreSum

crawling_tmp = crawling()

def homeView(request):
    context = None
    myTeam = []
    user_Info = User_Info.objects.get(user=request.user)
    course_id = user_Info.course_id
    course_name = Course.objects.get(id=course_id).course_name

    team_id = user_Info.team_id
    if team_id != None:
        infos = User_Info.objects.filter(team_id=team_id) #같은 조들 전부다 filter, 단 다른 과정의 조들과 충돌할 수 있으므로 제외시켜야된다.
        for i in infos:
            if Course.objects.get(id=i.course_id).course_name == course_name:
                myTeam.append(User.objects.get(id=i.user_id).first_name)

    context = {
        'images': crawling_tmp[0],
        'urls': crawling_tmp[1],
        'status': crawling_tmp[2],
        'n': range(len(crawling_tmp[0])),
        'course': course_name,
        'myTeam': myTeam,
        'teamName': team_id,
        'teamLength': range(len(myTeam)),
    }
    return render(request, 'home.html', context)

def teamView(request):
    return render(request,'team.html',None)

def teamJson(request):
    # 과정명 가져오기
    jsonObject = json.loads(request.body)
    course = jsonObject.get('course')
    # 해당 과정 명에 해당 하는 모든 인원 뽑아오기
    objs = list(Course.objects.filter(course_name=course))
    stu_dict={}
    for obj in objs:
        id = obj.id
        user_info = User_Info.objects.get(course_id=id)
        stu_dict[user_info.user.first_name] = user_info.score

    stu_sorted_dict = sorted(stu_dict.items(), key=lambda item: item[1], reverse=True)
    context = {
        'course': course,
        'student': stu_sorted_dict,
    }
    return JsonResponse(context)

def homeTeamJson(request):
    context={}
    jsonObject = json.loads(request.body)
    myTeam = jsonObject.get('myTeam')
    allTeam = jsonObject.get('allTeam')
    #User_info의 team_id('조'명)를 할당한다.
    for i, team in enumerate(allTeam, start=1):
        for each in team:
            user_info = User_Info.objects.get(user_id=User.objects.get(first_name=each).id)
            user_info.team_id = i
            user_info.save()
    return JsonResponse(context)

def joinView(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('firstname')
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')
        course_name = request.POST.get('course')
        score = scoreSum(request)
        if User.objects.filter(username=username):
            context = {'error':'이미 가입된 아이디 입니다.'}
        elif password != re_password:
            context['error'] = '비밀번호가 다릅니다.'
        else:
            user = User.objects.create_user(username=username, first_name=name, password=password)
            course = Course(course_name=course_name); course.save();
            user_info = User_Info(user=user, score=score, course=course); user_info.save();
            auth.login(request, user)
            return redirect("login")
    return render(request, 'join.html', context)

def editView(request):
    context = {}
    if request.method == "POST":
        user = request.user
        username = request.POST["username"]
        password = request.POST["password"]
        re_password = request.POST["re-password"]

        if not User.objects.filter(username=username):
            return render(request, 'edit.html', {"error": "등록된 아이디가 존재하지 않습니다."})
        if password == re_password:
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            context = {"error": "비밀번호가 다릅니다."}
    return render(request, 'edit.html', context)

def loginView(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            return render(request, 'login.html', {'error': '사용자 아이디 또는 패스워드가 틀립니다.'})
    else:
        return render(request, 'login.html')

def logoutView(request):
    return render(request,'login.html')

def uploadView(request):
    user_Info = User_Info.objects.get(user=request.user)
    course_id = user_Info.course_id
    course_name = Course.objects.get(id=course_id).course_name

    context = {"course": course_name}
    if request.method == "POST":
        print(request.user.id)
        upload = UploadFile(upload_id=request.user.id,title=request.POST['title'], file=request.FILES['file'])
        upload.save()
        context['success'] = "파일이 성공적으로 업로드 되었습니다."

    return render(request, 'upload.html', context)

def uploadListView(request):
    user_Info = User_Info.objects.get(user=request.user)
    course_id = user_Info.course_id
    course_name = Course.objects.get(id=course_id).course_name
    files = UploadFile.objects.filter(upload=request.user.id)
    titles = []
    file_names = []
    date = []
    for i in files:
        titles.append(i.title)
        file_names.append(os.path.basename(i.file.name).split("/")[0])
        date.append(i.upload_time.strftime("%Y/%m/%d %H:%M:%S"))
    context = {
        "course": course_name,
        "titles": titles,
        "files": file_names,
        "date": date,
        "n": range(len(titles)),
    }
    return render(request, 'uploadList.html',context)

def qnaView(request):
    return render(request,'qna.html',None)

def qnaWriteView(request):
    return render(request,'qnaWrite.html',None)

def guideView(request):
    return render(request,'guide.html',None)

