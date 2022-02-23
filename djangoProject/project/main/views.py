from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import datetime

def homeView(request):
    return render(request,'home.html',None)

def teamView(request):
    return render(request,'team.html',None)

def joinView(request):
    return render(request,'join.html',None)

def qnaView(request):
    return render(request,'qna.html',None)

def guideView(request):
    return render(request,'guide.html',None)
