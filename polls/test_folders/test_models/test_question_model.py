import datetime
from django.utils import timezone
from polls.models import Question
from django.urls import reverse



class TestQuestionModel:
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future
        """
        
        def test_was_published_recently_with_future_question(self):
                time = timezone.now() + datetime.timedelta(days=30)
                future_question = Question(pub_date=time)
                assert future_question.was_published_recently() == False
        
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        
        def test_was_published_recently_with_an_old_question(self):
                time = timezone.now() - datetime.timedelta(days=1, seconds=1)
                old_question = Question(pub_date=time)
                assert old_question.was_published_recently() == False
        
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        
        def test_was_published_recently_with_recent_question(self):
                time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
                recent_question = Question(pub_date=time)
                assert recent_question.was_published_recently() == True
