import datetime
from django.utils import timezone
from .models import Question

# Create your tests here.
import pytest
# class QuestionModelTests():

def test_was_published_recently_with_future_question():

        """
        was_published_recently() returns False for questions whose pub_date
        is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        assert future_question.was_published_recently == False

"""
was_published_recently() returns True for questions whose pub_date
is within the last day.
"""
