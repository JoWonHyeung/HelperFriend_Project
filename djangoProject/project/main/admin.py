from django.contrib import admin
from .models import User_Info, Course, UploadFile, Reply, Question, UniCourse

# Register your models here.

admin.site.register(Course)
admin.site.register(Reply)
admin.site.register(Question)
admin.site.register(UploadFile)
admin.site.register(UniCourse)


class User_InfoAdmin(admin.ModelAdmin):

    actions = ['separateTeam']

    @admin.action(description='팀분류')
    def separateTeam(modeladmin, request, queryset):
         pass


admin.site.register(User_Info,User_InfoAdmin)


admin.site.site_header = 'Helperfriend Admin Page'