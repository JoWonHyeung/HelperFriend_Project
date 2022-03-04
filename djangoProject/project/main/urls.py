from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from main.views import uploadList, upload, home, authentication, team, email, qna

urlpatterns = [
    path('home/',home.homeView,name='home'),
    path('home/homeInfoJson/', home.homeInfoJson, name='homeInfoJson'),
    path('login/', authentication.loginView, name='login'),
    path('logout/', authentication.logoutView,name='logout'),
    path('join/',authentication.joinView,name='join'),
    path('edit/',authentication.editView,name='edit'),
    path('edit/editJson',authentication.editJson,name='editJson'),
    path('team/homeTeamJson/',team.homeTeamJson,name='homeTeamJson'),
    path('team/',team.teamView,name='team'),
    path('team/teamJson/',team.teamJson,name='teamJson'),
    path('upload/',upload.uploadView,name='upload'),
    path('uploadList/',uploadList.uploadListView,name='uploadList'),
    path('uploadList/uploadDelete/<id>',uploadList.uploadListDelete,name='uploadDelete'),
    path('uploadList/uploadDownload/<id>',views.uploadList.uploadListDownload,name='uploadDownload'),
    path('email/', email.emailView, name='email'),
    path('qna/',qna.qnaView,name='qna'),
    path('qnaWrite/',qna.qnaWriteView,name='qnaWrite'),
    path('guide/',views.guideView,name='guide'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


