from django.shortcuts import render
from main.crawling import crawling
# Create your views here.
from django.http import HttpResponse
from django.template import loader
import datetime

def homeView(request):
    crawling_tmp = crawling()
    context = {
        'images': crawling_tmp[0],
        'urls': crawling_tmp[1],
        'status': crawling_tmp[2],
        'n': range(len(crawling_tmp[0])),
    }
    return render(request, 'home.html', context)

def teamView(request):
    return render(request,'team.html',None)

def joinView(request):
    return render(request,'join.html',None)

def qnaView(request):
    return render(request,'qna.html',None)

def guideView(request):
    return render(request,'guide.html',None)
