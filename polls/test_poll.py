import datetime
from django.utils import timezone
from .models import Question

# Create your tests here.
import pytest

"""
was_published_recently() returns False for questions whose pub_date
is in the future
"""


"""
was_published_recently() returns True for questions whose pub_date
is within the last day.
"""
