from polls.views import IndexView
from django.urls import reverse
from polls.models import Question
import pytest
import datetime
from django.test import Client
from django.utils import timezone

client = Client()


"""
Create a question with the given `question_text` and published the
given number of `days` offset to now (negative for questions published
in the past, positive for questions that have yet to be published).
"""


@pytest.fixture
def create_question():
    def _create_question(question, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question, pub_date=time)

    return _create_question


@pytest.mark.django_db
def test_fixture(create_question):

    q = create_question("test question", -5)
    assert q.question_text == "test question"


"""
If no questions exist, an appropriate message is displayed.
"""


@pytest.mark.django_db
def test_no_questions():
    response = client.get(reverse("polls:index"))

    assert response.status_code == 200
    assert "No polls are available." in response.content.decode("utf-8")
    assert list(response.context["latest_question_list"]) == []


"""
Questions with a pub_date in the past are displayed on the
index page.
"""


@pytest.mark.django_db
def test_past_question(create_question):
    create_question("Past question.", -30)

    response = client.get(reverse("polls:index"))
    print(create_question)
    assert response.status_code == 200
