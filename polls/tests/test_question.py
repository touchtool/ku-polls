"""Test Question model."""
import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    """Test question models."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        end_time = timezone.now() + datetime.timedelta(days=30)
        old_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = timezone.now() + datetime.timedelta(days=30)
        recent_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """is_published() returns False for question whose pub_date is in future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_old_question(self):
        """is_published() returns True for question whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        end_time = timezone.now() + datetime.timedelta(days=30)
        old_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_recent_question(self):
        """is_published() returns True for question whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = timezone.now() + datetime.timedelta(days=30)
        recent_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(recent_question.is_published(), True)

    def test_can_vote(self):
        """can_vote returns True for question whose pub_date is between starting date and end date."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = timezone.now() + datetime.timedelta(days=30)
        recent_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(recent_question.can_vote(), True)

    def test_can_vote_before_polls_published(self):
        """can_vote returns False for question whose pub_date is not yet published."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_is_expired(self):
        """can_vote returns False for question whose pub_date was ended."""
        time = timezone.now() - datetime.timedelta(days=-8)
        end_time = timezone.now() + datetime.timedelta(days=-1)
        recent_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(recent_question.can_vote(), False)
