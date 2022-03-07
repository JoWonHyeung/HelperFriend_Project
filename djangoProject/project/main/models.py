from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    course_name = models.CharField(max_length=45)
    def __str__(self):
        return f"id={self.id}, course_name={self.course_name}"

class User_Info(models.Model):
    user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    team_id = models.IntegerField(null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    email = models.CharField(max_length=150,null=True)
    habit = models.CharField(max_length=45,null=True)
    target = models.CharField(max_length=45,null=True)
    mbti = models.CharField(max_length=45,null=True)
    major = models.CharField(max_length=45,null=True)
    creditNum = models.CharField(max_length=45,null=True)
    def __str__(self):
        return f"user={self.user}, score={self.score},team_id={self.team_id}," \
               f"course_id={self.course},habit={self.habit},target={self.target},mbti={self.mbti},major={self.major}, creditNum={self.creditNum}, email={self.email}"

class Question(models.Model):
    title = models.CharField(max_length=45)
    question_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)
    questionuser = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f"id={self.id}, title={self.title}, question_time={self.question_time}, questionuser={self.questionuser_id}"

class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    replyuser = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    comment_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"id={self.id}, question={self.question}, replyuser_id={self.replyuser}, comment={self.comment},comment_time={self.comment_time}"

class UploadFile(models.Model):
    upload = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100,null=True)
    upload_time = models.DateTimeField(auto_now=True)
    file = models.FileField(blank=True, null=True,upload_to="file_%Y_%m_%d")
    def __str__(self):
        return f"id={self.id}, upload={self.upload}, title={self.title}, upload_time={self.upload_time},file={self.file}"