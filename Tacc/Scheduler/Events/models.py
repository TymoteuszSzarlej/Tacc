from django.db import models


class EventType(models.Model):
    name = models.CharField(max_length=100)
    is_recurring = models.BooleanField(default=False)
    recurrence_interval_days = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Liczba dni między powtórzeniami (np. 7 = co tydzień)"
    )
    recurrence_weekdays = models.JSONField(
        null=True, blank=True,
        help_text="Lista dni tygodnia, np. ['Monday', 'Wednesday']"
    )

    def __str__(self):
        return self.name


class EventTag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(
        max_length=7,
        default="#CCCCCC",
        help_text="Kolor HEX, np. #FF5733"
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True)
    event_type = models.ForeignKey(
        EventType,
        on_delete=models.CASCADE,
        related_name='events'
    )
    location = models.CharField(max_length=255)
    tags = models.ManyToManyField(
        EventTag,
        related_name='events',
        blank=True
    )

    def __str__(self):
        return self.name


class EventReminder(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='reminders'
    )
    reminder_time = models.DateTimeField()

    def __str__(self):
        return f"Reminder for {self.event.name} at {self.reminder_time}"


class EventNote(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.event.name} ({self.created_at.strftime('%Y-%m-%d')})"
