from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    class Meta:
        ordering = ['-id']

    title = models.CharField('Title', max_length=100, default=None, null=False, blank=False)
    is_finished = models.BooleanField('Finished', default=False)
    success = models.BooleanField('Success', default=False)
    created_by = models.ForeignKey(User, default=None, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='tasks_created')
    content = models.CharField('Title', max_length=100, default=None, null=False, blank=False)

    def complete(self):
        self.is_finished = True
        self.success = True
        self.save()

    def cancel(self):
        self.is_finished = True
        self.success = False
        self.save()

    def __str__(self):
        return f'{self.title}{" ✓" if self.is_finished and self.success else " ✖" if self.is_finished and not self.success else ""}'
