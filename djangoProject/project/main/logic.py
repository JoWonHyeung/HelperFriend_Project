from django.contrib.auth.models import User
from django.contrib import auth

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
