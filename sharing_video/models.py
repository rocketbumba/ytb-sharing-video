from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class SharingVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    video_url = models.URLField()


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    video_url = models.URLField()
    type = models.CharField(max_length=100)