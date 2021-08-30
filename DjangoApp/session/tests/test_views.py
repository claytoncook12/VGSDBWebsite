# session/tests/test_views.py

import pytest

from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
class TestHomeView:
    def test_shows_home(self):
        """The session view should show the session title."""
        
        client = Client()
        response = client.get(reverse('home'))
        assert response.status_code == 200