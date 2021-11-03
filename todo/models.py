from django.db import models


class Task(models.Model):
    class Meta:
        ordering = ['-id']

    title = models.CharField('Title', max_length=100, default=None, null=False, blank=False)
    is_finished = models.BooleanField('Finished', default=False)

    def finish(self):
        self.is_finished = True

    def __str__(self):
        return f'{self.title} {"✓" if self.is_finished else ""}'
