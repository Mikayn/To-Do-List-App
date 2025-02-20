from django.db import models

class Tasks(models.Model):
    task = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task} - {'Completed' if self.status else 'Pending'}"