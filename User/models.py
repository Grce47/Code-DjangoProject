from django.db import models
from django.contrib.auth.models import User


class pythonCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    codearea = models.TextField()
    output = models.TextField()
    session_key = models.TextField(null=True)
    added = models.DateTimeField(auto_now_add=True)
    Done = models.BooleanField(default=False)
    Feedback = models.CharField(null=True, default="", max_length=100)

    def __str__(self):
        return self.added.strftime('%Y-%m-%d %H:%M')

    class Meta:
        ordering = ['-added']
