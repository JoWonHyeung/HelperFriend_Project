from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.models import User_Info, UploadFile, Question, Course, Reply, UniCourse
from main.logic import scoreSum, emailSend, verificationMailSend, crawling, uploadListUpdate
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator
import urllib
import json
import os.path
from django.http import HttpResponseRedirect
from django.urls import reverse

crawling = crawling()

class home:
    @login_required(login_url='/main/login/')
    def homeView(request):
        context = None
        user_Info = User_Info.objects.get(user=request.user)
        home_user = {}; crawling_info = {}
        course_name = Course.objects.get(id=user_Info.course_id).course_name
        #홈 화면에 나타나는 팀 정보들을 띄워주기 위해서 팀원 정보들을 뽑아낸다.
        if user_Info.team_id != None:
            infos = User_Info.objects.filter(team_id=user_Info.team_id)
            for i in infos: # 같은 조들 전부다 filter, 단 다른 과정의 조들과 충돌할 수 있으므로 제외시켜야된다.
                if Course.objects.get(id=i.course_id).course_name == course_name:
                    home_user[User.objects.get(id=i.user_id).username] = [User.objects.get(id=i.user_id).first_name,
                                                                          i.habit, i.target, i.mbti, i.major, User.objects.get(id=i.user_id).username,
                                                                          course_name]
        context = {
            'crawling': crawling,
            'home_user': home_user,
        }
        return render(request, 'home.html', context)

    #홈 화면 개인정보 가져오기
    def homeInfoJson(request):
        user_Id = json.loads(request.body).get('id')
        user_Info = User_Info.objects.get(user_id=user_Id)
        context = {
            'id': user_Info.user.username,
            'name': user_Info.user.first_name,
            'course': Course.objects.get(id=user_Info.course_id).course_name,
        }
        return JsonResponse(context)

    #홈 화면 게시판 글 3개 가져오기
    def homeBoardJson(request):
        return JsonResponse({'home_board': list(Question.objects.all().order_by('-question_time')[:3].values())})

class authentication:
    def loginView(request):
        if request.method == "POST":
            user = auth.authenticate(username=request.POST.get('username', None),
                                     password=request.POST.get('password', None))
            if user is not None:
                auth.login(request, user)
                return redirect("home")
            else:
                return render(request, 'login.html', {'error': '사용자 아이디 또는 패스워드가 틀립니다.'})
        else:
            return render(request, 'login.html')

    def logoutView(request):
        return render(request, 'login.html')

    def pwdeditView(request):
        return render(request, 'pwdedit.html')

    def ideditView(request):
        return render(request, 'idedit.html')

    def pwdEditJson(request):
        context = {}
        if json.loads(request.body).get('username'):
            user_username = json.loads(request.body).get('username')
            try:
                User.objects.get(username=user_username)
                context = {'idMsg': '아이디 인증완료'}
            except User.DoesNotExist:
                context = {'idMsg': '아이디가 존재하지 않습니다.'}
        elif json.loads(request.body).get('email'):
            input_email = json.loads(request.body).get('email')
            user_username = json.loads(request.body).get('emailusername')

            user_email = User_Info.objects.get(user=User.objects.get(username=user_username)).email

            if user_email == input_email:
                context = {'emailMsg': '이메일 인증완료'}
                # 인증번호 메일 전송 및 DB에 인증번호 저장
                verificationMailSend(user_email, user_username, "[HelperFriend] 비밀번호 인증 메일입니다.")
            else:
                context = {'emailMsg': '이메일이 존재하지 않습니다.'}
        elif json.loads(request.body).get('creditNum'):
            user_credit = json.loads(request.body).get('creditNum')
            user_username = json.loads(request.body).get('creditusername')
            if user_credit == User_Info.objects.get(user=User.objects.get(username=user_username)).creditNum:
                context = {'creditMsg': '확인 완료'}
            else:
                context = {'creditMsg': '인증번호가 다릅니다.'}
        elif json.loads(request.body).get('pwd'):
            change_pwd = json.loads(request.body).get('pwd')
            user_username = json.loads(request.body).get('pwdusername')

            user = User.objects.get(username=user_username)
            user.set_password(change_pwd)
            user.save()
        return JsonResponse(context)

    def idEditJson(request):
        context={}
        if json.loads(request.body).get('email'):
            user_email = json.loads(request.body).get('email')
            try:
                user_info = User_Info.objects.get(email=user_email)
                user_username = user_info.user.username
                context = {
                    'emailMsg': '이메일 인증완료',
                    'username': user_username,
                    'userId': user_info.user_id
                }
                verificationMailSend(user_email, user_username, "[HelperFriend] 아이디 인증 메일입니다.")
            except User_Info.DoesNotExist:
                context = {'emailMsg': '이메일이 존재하지 않습니다.'}
        elif json.loads(request.body).get('creditNum'):
            creditNum = json.loads(request.body).get('creditNum')
            user_id = json.loads(request.body).get('userId')
            user = User.objects.get(id=user_id)
            if creditNum == User_Info.objects.get(user=user).creditNum:
                context = {
                    'username': user.username,
                    'creditMsg': "인증번호가 일치합니다."
                }
            else:
                context = {'creditMsg': "인증번호가 일치하지 않습니다."}
        return JsonResponse(context)

    def joinView(request): #회원가입
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            name = request.POST.get('firstname')
            email = request.POST.get('joinemail')
            password = request.POST.get('password')
            re_password = request.POST.get('re-password')
            course_name = request.POST.get('course')
            habit = request.POST.get('habit')
            major = request.POST.get('univ')
            mbti = request.POST.get('mbti')
            target = request.POST.get('target')
            score = scoreSum(request)

            if User.objects.filter(username=username):
                context = {'error': '이미 가입된 아이디 입니다.'}
            elif password != re_password:
                context = {'error': '비밀번호가 다릅니다.'}
            else:
                user = User.objects.create_user(username=username, first_name=name, password=password)
                course = Course(course_name=course_name)
                course.save()
                user_info = User_Info(user=user, score=score, course=course, habit=habit, major=major, mbti=mbti,
                                      target=target, email=email)
                user_info.save()
                auth.login(request, user)
                return redirect("login")
        return render(request, 'join.html', context)

    def joinJson(request):
        course = []
        for i in UniCourse.objects.all():
            course.append(i.course_uniname)
        return JsonResponse({'course':course})


class team:
    def teamView(request):
        return render(request, 'team.html', None)

    def teamJson(request):
        # 과정명 가져오기]
        course = json.loads(request.body).get('course')
        # 해당 과정 명에 해당 하는 모든 인원 뽑아오기
        students = list(Course.objects.filter(course_name=course))
        stu_list = []
        #동명이인 처리 => dict 중복 불가!
        for student in students:
            user_info = User_Info.objects.get(course_id=student.id)
            stu_list.append((user_info.user.first_name, user_info.score, user_info.user_id))

        stu_sorted_dict = sorted(stu_list, key=lambda item: item[1], reverse=True)

        context = {
            'course': course,
            'student': stu_sorted_dict,
        }
        return JsonResponse(context)

    def homeTeamJson(request):
        jsonObject = json.loads(request.body)
        myTeam = jsonObject.get('myTeam')
        allTeam = jsonObject.get('allTeam')

        # User_info의 team_id('조'명)를 할당한다.
        for i, team in enumerate(allTeam, start=1):
            for each in team:
                user_info = User_Info.objects.get(user_id=User.objects.get(id=each[1]))
                user_info.team_id = i
                user_info.save()
        return JsonResponse({})

class upload:
    def uploadView(request):
        context = {}
        if request.method == "POST":
            if not request.FILES.get('file'):
                context = {
                    'fileMsg': '파일을 업로드 해주세요',
                    'color': 'red'
                }
            else:
                upload = UploadFile(upload_id=request.user.id, title=request.POST.get('title'),
                                    file=request.FILES.get('file'))
                upload.save()
                context = {
                    'fileMsg': '파일을 성공적으로 업로드 하였습니다.',
                    'color': 'blue'
                }
        return render(request, 'upload.html', context)


class uploadList():
    def uploadListView(request):
        context = uploadListUpdate(request)
        return render(request, 'uploadList.html', context)

    def uploadListDelete(request, id):
        # 삭제
        upload_file = UploadFile.objects.get(id=id)
        upload_file.delete()
        # 삭제 후 update
        context = uploadListUpdate(request)
        return render(request, 'uploadList.html', context)

    def uploadListDownload(request, id):
        file = UploadFile.objects.get(id=id).file
        file_path = os.path.join(os.getcwd() + "\\media\\")
        file_name = file.name.replace('/', '\\').split('\\')
        response = FileResponse(FileSystemStorage(file_path + file_name[0]).open(file_name[1], 'rb'),
                                content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % urllib.parse.quote(file_name[1].encode('utf-8'))
        return response

class email:
    def emailView(request):
        if request.method == 'POST':
            emailSend(request)
            return redirect('home')
        else:
            return render(request, 'email.html')

class qna:
    @login_required(login_url='/main/login/')
    def qnaListView(request):
        page = request.GET.get('page',1)
        vlist = Question.objects.all().order_by('-question_time')
        paginator = Paginator(vlist,10)
        vlistpage = paginator.get_page(page)
        context = {
            "vlist": vlistpage,
            'pages': range(1, vlistpage.paginator.num_pages + 1)
        }
        return render(request,'qnaList.html',context)

    @login_required(login_url='/main/login/')
    def qnaWriteView(request):
        if request.method == 'POST':
            user = request.user # 작성자: 현재 로그인 되어 있는 사람
            title = request.POST.get('title')
            content = request.POST.get('context')
            Question(questionuser=user, content=content, title=title, question_username=request.user.username).save()
            return redirect('qnaList')
        else:
            return render(request, 'qnaWrite.html', None)

    @login_required(login_url='/main/login/')
    def qnaReadAndReplyView(request, qnaId):
        context = {}
        if request.method == "POST": #reply 저장
            content = request.POST.get('replyContent')
            Reply(question_id=qnaId, replyuser_id=request.user.id, comment=content).save()
        elif request.GET.get('replypk') : #댓글 삭제
            try:
                Reply.objects.get(id=request.GET.get('replypk')).delete()
            except Reply.DoesNotExist:
                pass
        elif request.GET.get('editreplypk'): #댓글 수정
            try:
                reply = Reply.objects.get(id=request.GET.get('editreplypk'))
                reply.comment = request.GET.get('reply')
                reply.save()
            except:
                pass
        elif request.GET.get('boardpk'): #게시판 삭제
            try:
                boardpk = request.GET.get('boardpk')
                Question.objects.get(id=boardpk).delete()
                return redirect('qnaList')
            except Question.DoesNotExist:
                pass
        qna = Question.objects.get(id=qnaId)
        context = {'data': qna}
        return render(request, 'qnaRead.html', context)

    def qnaEditView(request):
        qnaId = request.GET.get('boardpk',None)
        qna = Question.objects.get(id=qnaId)
        title = ""; content = ""
        context = {}
        if request.method == "POST": #저장하기
            qna.title = request.POST.get("title")
            qna.content = request.POST.get("text")
            qna.save()
            return HttpResponseRedirect('/main/qna/qnaReadAndReply/' + qnaId)
        else: #보여주기
            title = qna.title
            content = qna.content
            context = {
                'id': qnaId,
                'title': title,
                'content': content,
            }
        return render(request, 'qnaEdit.html',context)


    def qnaReplyJson(request,qnaId): #해당 게시물에 대한 모든 댓글들 다 끌어오기
        replys = Reply.objects.filter(question_id=qnaId)
        username = []; content = []; id = [];
        for reply in replys:
            username.append(reply.replyuser.username)
            content.append(reply.comment)
            id.append(reply.id)
        context = {
            'username': username,
            'content': content,
            'replyId': id,
        }
        return JsonResponse(context)

