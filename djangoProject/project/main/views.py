import json
import os.path
import smtplib, ssl
from main.crawling import crawling
from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.models import User_Info, UploadFile
from main.models import Course
from django.contrib.auth.models import User
from django.contrib import auth
from main.logic import scoreSum
from django.contrib.auth.decorators import login_required
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

crawling_tmp = crawling()

@login_required(login_url='/main/login/')
def homeView(request):
    context = None
    user_Info = User_Info.objects.get(user=request.user)
    course_name = Course.objects.get(id=user_Info.course_id).course_name
    habit = []; target = []; mbti = []; major = []; name = []; myId = []

    #홈 화면에 나타나는 팀 정보들을 띄워주기 위해서 팀원 정보들을 뽑아낸다.
    if user_Info.team_id != None:
        infos = User_Info.objects.filter(team_id=user_Info.team_id)
        for i in infos: # 같은 조들 전부다 filter, 단 다른 과정의 조들과 충돌할 수 있으므로 제외시켜야된다.
            if Course.objects.get(id=i.course_id).course_name == course_name:
                # User_info에 접근해서 같은 팀원들의 정보들을 뽑아온다.
                habit.append(i.habit); target.append(i.target); mbti.append(i.mbti); major.append(i.major)
                name.append(User.objects.get(id=i.user_id).first_name)
                myId.append(User.objects.get(id=i.user_id).username)

    context = {
        'images': crawling_tmp[0],
        'urls': crawling_tmp[1],
        'status': crawling_tmp[2],
        'n': range(len(crawling_tmp[0])),
        'course': course_name,
        'name': name,
        'habit': habit,
        'target': target,
        'mbti': mbti,
        'major': major,
        'Id': myId,
        'teamName': user_Info.team_id,
        'teamLen': range(len(name)),
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
        habit = request.POST.get('habit')
        major = request.POST.get('univ')
        mbti = request.POST.get('mbti')
        target = request.POST.get('target')

        score = scoreSum(request)
        if User.objects.filter(username=username):
            context = {'error':'이미 가입된 아이디 입니다.'}
        elif password != re_password:
            context['error'] = '비밀번호가 다릅니다.'
        else:
            user = User.objects.create_user(username=username, first_name=name, password=password)
            course = Course(course_name=course_name); course.save();
            user_info = User_Info(user=user, score=score, course=course,habit=habit,major=major,mbti=mbti,target=target); user_info.save();
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
        upload = UploadFile(upload_id=request.user.id,title=request.POST.get('title'), file=request.FILES.get('file'))
        upload.save()
        context['success'] = "파일이 성공적으로 업로드 되었습니다."
    return render(request, 'upload.html', context)

def uploadListView(request):
    user_Info = User_Info.objects.get(user=request.user)
    course_id = user_Info.course_id
    course_name = Course.objects.get(id=course_id).course_name
    files = UploadFile.objects.filter(upload=request.user.id)
    file_titles = []; file_names = []; file_ids = []; file_date = []
    for i in files:
        file_titles.append(i.title)
        file_ids.append(i.id)
        file_names.append(os.path.basename(i.file.name).split("/")[0])
        file_date.append(i.upload_time.strftime("%Y/%m/%d"))
    context = {
        "course": course_name,
        "titles": file_titles,
        "names": file_names,
        "date": file_date,
        "ids": file_ids,
        "n": range(len(file_titles)),
    }
    return render(request, 'uploadList.html',context)

def uploadListDelete(request,id):
    #삭제
    upload_file = UploadFile.objects.get(id=id)
    upload_file.delete()
    #update
    user_Info = User_Info.objects.get(user=request.user)
    course_id = user_Info.course_id
    course_name = Course.objects.get(id=course_id).course_name
    files = UploadFile.objects.filter(upload=request.user.id)
    file_titles = []; file_names = []; file_ids = []; file_date = []
    for i in files:
        file_titles.append(i.title)
        file_ids.append(i.id)
        file_names.append(os.path.basename(i.file.name).split("/")[0])
        file_date.append(i.upload_time.strftime("%Y/%m/%d"))
    context = {
        "course": course_name,
        "titles": file_titles,
        "names": file_names,
        "date": file_date,
        "ids": file_ids,
        "n": range(len(file_titles)),
    }
    return render(request, 'uploadList.html', context)

from django.views.generic.detail import SingleObjectMixin
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
import magic
import mimetypes
import urllib

def uploadListDownload(request, id):
    file = UploadFile.objects.get(id=id).file
    file_path = os.path.join(os.getcwd() + "\\media\\")
    file_name = file.name.replace('/','\\').split('\\')
    #print(mimetypes.MimeTypes().guess_type(file.file.name)[0])
    print(file_name)
    print(file_path)
    fs = FileSystemStorage(file_path + file_name[0])
    response = FileResponse(fs.open(file_name[1],'rb'), content_type='application/force-download')
    print(file_name[1])
    print(f'attachment; filename="{ file_name[1] }"')

    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % urllib.parse.quote(file_name[1].encode('utf-8'))
    #*=UTF-8\’\’%s’ % urllib.quote(filename.encode(‘utf-8’))
    return response

def emailView(request):
    user_Info = User_Info.objects.get(user=request.user)
    course_id = user_Info.course_id
    course_name = Course.objects.get(id=course_id).course_name
    if request.method == 'POST':
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = 'wonhyeongjo60@gmail.com'
        receiver_email = request.POST.get('email')
        password = "bhghvqcwzoiswuff"
        title = request.POST.get('title')
        message = request.POST.get('text')
        file = request.FILES.get('file')

        extense = file.name.split('.')[1]

        msg = MIMEMultipart()
        msg['Subject'] = title
        msg.attach(MIMEText(message, 'plain'))

        if extense == "jpg" or extense == 'png':
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + file.name)
            msg.attach(part)
        else:
            msg.attach(MIMEApplication(file.file.read(),Name=file.name))

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return redirect('home')
    else:
        return render(request,'email.html',{"course": course_name})

def qnaView(request):
    return render(request,'qna.html',None)

def qnaWriteView(request):
    return render(request,'qnaWrite.html',None)

def guideView(request):
    return render(request,'guide.html',None)

