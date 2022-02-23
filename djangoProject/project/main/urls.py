from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.homeView,name = 'home'),
    path('join/',views.joinView,name = 'join'),
    path('qna/',views.qnaView,name='qna'),
    path('team/',views.teamView,name='team'),
    path('guide/',views.guideView,name='guide'),
]
