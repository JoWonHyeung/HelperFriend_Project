from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import smtplib, ssl

def scoreSum(request):
    score = 0
    major = request.POST.get("major")
    if major == "IT":
        score = 5  # 기본 점수
        project = request.POST.get("project")
        award = request.POST.get("award")
        problem = request.POST.get("problem1")
        # 1-1 프로젝트 경험 횟수
        if project == "1":
            score += float(project)
        elif project == "0.5":
            score += float(project)
        elif project == "0.1":
            score += float(project)
        # 1-2 교내 및 교외 수상 횟수
        if award == '3':
            score += float(award)
        elif award == '1':
            score += float(award)

        # 1-3 문제 푼 개수
        if problem == "3":
            score += float(problem)
        elif problem == "1":
            score += float(problem)
        elif problem == "0.5":
            score += float(problem)
    elif major == "c-IT":
        score = 2  # 기본 점수
        lesson = request.POST.get("lesson")
        problem = request.POST.get("problem2")
        award = request.POST.get("award2")
        # 2-1 코딩 관련 수업을 들은 적이 있습니까?
        if lesson == "3":
            score += float(lesson)
        elif lesson == "0.5":
            score += float(lesson)
        elif lesson == "0.1":
            score += float(lesson)
        # 2-2 문제 푼 경험
        if problem == '3':
            score += float(problem)
        elif problem == '1':
            score += float(problem)
        # 2-3 수상경험
        if award == "3":
            score += float(award)
    else:
        score = 0  # 기본 점수
        experience = request.POST.get("exper")
        project = request.POST.get("project2")
        award = request.POST.get("award3")
        # 3-1 코딩 경험 유무
        if experience == "2":
            score += float(experience)
        # 3-2 프로젝트 경험 횟수
        if project == '5':
            score += float(project)
        elif project == '3':
            score += float(project)
        # 3-3 수상 경력
        if award == "3":
            score += float(award)
        elif award == "1":
            score += float(award)
    return score

def emailSend(request):
    msg = MIMEMultipart()
    message = request.POST.get('text')
    file = request.FILES.get('file')

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    msg['From'] = 'helperfriend32@gmail.com'
    msg['To'] = request.POST.get('email')
    msg['Subject'] = "[" + request.user.first_name + "] [" + datetime.today().strftime(
        "%Y/%m/%d %H:%M:%S") + "] " + request.POST.get('title')
    msg.attach(MIMEText(message, 'plain'))
    password = "vlmakurzryemowff"

    # 수신자가 없거나, 파일이 존재하지 않으면 home화면으로 redirect
    if file != None and msg['To'] != "":
        extense = file.name.split('.')[1]
        # 확장자 별로 다르게 처리
        if extense == "jpg" or extense == 'png':
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + file.name)
            msg.attach(part)
        else:
            msg.attach(MIMEApplication(file.file.read(), Name=file.name))

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(msg['From'], password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
