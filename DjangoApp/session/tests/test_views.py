# Session/tests/test_views.py

import pytest

from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
class TestHomeView:
    def test_session_home_200(self):
        client = Client()
        response = client.get(reverse('home'))
        assert response.status_code == 200, "Get 200 status For session.views.home"

class TestAboutView:
    def test_session_about_200(self):
        client = Client()
        response = client.get(reverse('about'))
        assert response.status_code == 200, "Get 200 status for session.views.about"

@pytest.mark.django_db
class TestFullYtSessionList:
    def test_session_full_yt_session_list_200(self):
        client = Client()
        response = client.get(reverse('full_yt_session_list'))
        assert response.status_code == 200, "Get 200 status for session.views.full_yt_session_list"
