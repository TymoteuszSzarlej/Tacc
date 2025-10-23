from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100)
    is_recurring = models.BooleanField(default=False)
    recurrence_interval_days = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Liczba dni między powtórzeniami (np. 3 = co 3 dni)"
    )
    recurrence_weekdays = models.JSONField(
        null=True, blank=True,
        help_text="Lista dni tygodnia, np. ['Tuesday', 'Friday']"
    )

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    task_status = models.ForeignKey(
        TaskStatus,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks'
    )

    def __str__(self):
        return self.title


class TaskLog(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    log_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"Log for {self.task.title} ({self.log_date.strftime('%Y-%m-%d')})"


class TaskAttachment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.task.title}"