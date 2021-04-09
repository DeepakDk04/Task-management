from django.db import models

from account.models import Profile
# Create your models here.


class Task(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default="")
    name = models.TextField()
    done = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
