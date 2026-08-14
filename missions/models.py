from django.db import models

from django.conf import settings


# Create your models here.

class Role(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    points = models.PositiveIntegerField(default=0)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Goal(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    target_outcome = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.target_outcome


class Block(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    difficulty = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
