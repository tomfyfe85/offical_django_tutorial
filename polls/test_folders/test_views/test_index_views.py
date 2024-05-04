from polls.views import IndexView
from django.urls import reverse
from polls.models import Question
import pytest
import datetime
from django.test import Client
from django.utils import timezone

client = Client()


@pytest.fixture
def create_question():
    def _create_question(question, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question, pub_date=time)

    return _create_question


class TestQuestionIndexView:
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """

    @pytest.mark.django_db
    def test_fixture(self, create_question):

        q = create_question("test question?", -5)
        assert q.question_text == "test question?"

    """
    If no questions exist, an appropriate message is displayed.
    """

    @pytest.mark.django_db
    def test_no_questions(self):
        response = client.get(reverse("polls:index"))

        assert response.status_code == 200
        assert "No polls are available." in response.content.decode("utf-8")
        assert list(response.context["latest_question_list"]) == []

    """`
    Questions with a pub_date in the past are displayed on the
    index page.
    """

    @pytest.mark.django_db
    def test_past_question(self, create_question):
        q = create_question("Past question.", -30)
        response = client.get(reverse("polls:index"))

        assert response.status_code == 200
        assert list(response.context["latest_question_list"]) == [q]

    """
    Questions with a pub_date in the future aren't displayed on
    the index page.
    """

    @pytest.mark.django_db
    def test_future_question(self, create_question):
        q = create_question("future question.", 30)
        response = client.get(reverse("polls:index"))
        assert list(response.context["latest_question_list"]) == []

    """
    Even if both past and future questions exist, only past questions
    are displayed.
    """

    @pytest.mark.django_db
    def test_future_question_and_past_question(self, create_question):
        q = create_question("Past question.", -30)
        create_question("future question.", 30)
        response = client.get(reverse("polls:index"))
        assert list(response.context["latest_question_list"]) == [q]

    """
    The questions index page may display multiple questions.
    """

    @pytest.mark.django_db
    def test_two_past_questions(self, create_question):
        q1 = create_question("Past question 1.", -30)
        q2 = create_question("Past question 2.", -5)
        response = client.get(reverse("polls:index"))
        assert list(response.context["latest_question_list"]) == [q2, q1]


class TestDetailViewTests:
    """
    The detail view of a question with a pub_date in the future
    returns a 404 not found.
    """

    @pytest.mark.django_db
    def test_future_question(self, create_question):

        future_question = create_question("future question", 5)
        response = client.get(reverse("polls:detail", args=[future_question.id]))
        assert response.status_code == 404
