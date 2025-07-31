# pollpro_backend/polls/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Poll(models.Model):
    CATEGORY_CHOICES = (
        ('TECH', 'Technology'),
        ('ENT', 'Entertainment'),
        ('SPRT', 'Sports'),
        ('POL', 'Politics'),
        ('LIFE', 'Lifestyle'),
        ('EDU', 'Education'),
    )
    question = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES, default='TECH')
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.question

    def is_active(self):
        return self.expiry_date is None or self.expiry_date > timezone.now()

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.poll.question} - {self.text}"

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'user')

    def clean(self):
        if not self.poll.is_active():
            raise ValidationError("Cannot vote on an expired poll.")

    def __str__(self):
        return f"{self.user.username} voted for {self.option.text} in {self.poll.question}"