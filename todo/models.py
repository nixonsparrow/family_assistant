from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100, default=None, null=False, blank=False)
