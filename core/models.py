from django.db import models

class TaskManager(models.Model):
    title = models.CharField(max_length=200)
    priority = models.CharField(max_length=50, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
from django.utils import timezone


class DailyTask(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class DailyTaskLog(models.Model):
    task = models.ForeignKey(DailyTask, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('task', 'date')

    def __str__(self):
        return f"{self.task.title} - {self.date}"
class ExpenseTracker(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason
