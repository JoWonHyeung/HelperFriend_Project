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
    def __str__(self):
        return f"user={self.user}, score={self.score},team_id={self.team_id},course_id={self.course}"

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

