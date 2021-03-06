"""Models for poll app."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """Question with question_text, pub_date and end_date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date expired', null=True)

    def __str__(self):
        """Return question_text as string."""
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """Return true if current date is in between yesterday and this day."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return true if current date is on or after question’s publication date."""
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Return true if voting is currently allowed for this question."""
        now = timezone.now()
        if self.end_date is None:
            return self.pub_date <= now
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """Choice with question, choice_text and votes."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choice_text as string."""
        return self.choice_text

    @property
    def votes(self) -> int:
        """Return number of vote count."""
        count = Votes.objects.filter(choice=self).count()
        return count


class Votes(models.Model):
    """Vote one per id."""

    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,
                             null=False,
                             blank=False,
                             on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        """Display vote by user."""
        return f"Vote by {self.user.username} for {self.choice.choice_text}"
