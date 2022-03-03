from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/',views.homeView,name='home'),
    path('homeTeamJson/',views.homeTeamJson,name='homeTeamJson'),
    path('join/',views.joinView,name='join'),
    path('login/',views.loginView,name='login'),
    path('logout/',views.logoutView,name='logout'),
    path('upload/',views.uploadView,name='upload'),
    path('uploadList/',views.uploadListView,name='uploadList'),
    path('uploadList/uploadDelete/<id>',views.uploadListDelete,name='uploadDelete'),
    path('uploadList/uploadDownload/<id>',views.uploadListDownload,name='uploadDownload'),
    path('email/', views.emailView, name='email'),
    path('edit/',views.editView,name='edit'),
    path('qna/',views.qnaView,name='qna'),
    path('team/',views.teamView,name='team'),
    path('teamJson/',views.teamJson,name='teamJson'),
    path('guide/',views.guideView,name='guide'),
    path('qnaWrite/',views.qnaWriteView,name='qnaWrite'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
