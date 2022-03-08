from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
from django.contrib.auth.models import User
from main.models import User_Info
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import smtplib, ssl
import random

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
    msg['Subject'] = "[HelperFriend]" + "[" + request.user.first_name + "]" + "[" + datetime.today().strftime("%Y/%m/%d %H:%M:%S") + "] " + request.POST.get('title')
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

def verificationMailSend(email, username, title):
    msg = MIMEMultipart()
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    msg['From'] = 'helperfriend32@gmail.com'
    msg['To'] = email
    msg['Subject'] = title
    msg['password'] = "vlmakurzryemowff"
    randomNum = str(random.randint(1000,9999))
    message = "인증번호: " + "[" + randomNum + "]"
    msg.attach(MIMEText(message, 'plain'))

    #인증번호 DB에 저장
    user_Info = User_Info.objects.get(user=User.objects.get(username=username))
    user_Info.creditNum = randomNum;
    user_Info.save()

    #전송
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(msg['From'], msg['password'])
        server.sendmail(msg['From'], msg['To'], msg.as_string())

def crawling():
    # 1
    query_txt = "AI"

    status = []
    # 2
    chrome_path = "c://tmp//chromedriver.exe"

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(chrome_path, options=options)
    driver.get("https://thinkyou.co.kr/index.asp")
    driver.maximize_window()
    time.sleep(3)

    # 3
    a = ActionChains(driver)
    m = driver.find_element_by_xpath('//*[@id="gnb"]/li[1]/a/span')
    a.move_to_element(m).perform()
    time.sleep(0.5)

    # 4
    driver.find_element_by_xpath('//*[@id="gnb"]/li[1]/ul/li[1]').click()

    driver.find_element_by_xpath('//*[@id="searchFrm"]/div/div/div[1]/select').click()
    driver.find_element_by_xpath('//*[@id="searchFrm"]/div/div/div[1]/select/option[2]').click()

    driver.find_element_by_xpath('//*[@id="searchFrm"]/div/div/div[1]/span/input[1]').click()
    elem = driver.find_element_by_name("searchstr")
    elem.send_keys(query_txt)
    elem.send_keys("\n")
    time.sleep(2)

    # driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/a[3]').click() #참석중 클릭
    # time.sleep(1)

    # 5. url수집
    urls = []
    default_dir = "https://thinkyou.co.kr"
    res = {}

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    all = soup.find('div', 'contestArea')

    allTag = all.find_all('div', 'title')
    allStatus = all.find_all('div', 'statNew')

    for i in allTag:
        a_tag = i.find('a')['href']
        urls.append(default_dir + a_tag)

    for i in allStatus:
        status_tag = i.find('p').get_text()
        status.append(status_tag)
    # 6
    urls_image = []

    import sys
    from urllib.parse import quote

    bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    file_no = 1

    for num in range(0,6):
        driver.get(urls[num])  # 사이트 접속

        html1 = driver.page_source
        soup1 = BeautifulSoup(html1, 'html.parser')

        # Title 수집
        title = soup1.find('dl', 'title').find('h1').get_text()

        # 이미지 확대
        driver.find_element_by_xpath('//*[@id="printArea"]/div[1]/div/div[1]/img').click()

        html2 = driver.page_source
        soup2 = BeautifulSoup(html2, 'html.parser')

        # 이미지 수집
        try:
            photo = soup2.find('div', 'galleryImg').find('img')['src']
        except:
            continue
        else:
            full_image = 'https://thinkyou.co.kr/' + quote(photo)
            urls_image.append(full_image)
            file_no += 1
        time.sleep(1)
    for i in range(0,6):
        res[str(i)] = [urls_image[i], urls[i], status[i]]
    return res