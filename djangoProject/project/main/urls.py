from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.homeView,name='home'),
    path('join/',views.joinView,name = 'join'),
    path('login/',views.loginView,name = 'login'),
    path('edit/',views.editView,name='edit'),
    path('qna/',views.qnaView,name='qna'),
    path('team/',views.teamView,name='team'),
    path('teamJson/',views.teamJson,name='teamJson'),
    path('guide/',views.guideView,name='guide'),
    path('qnaWrite/',views.qnaWriteView,name='qnaWrite'),
]
