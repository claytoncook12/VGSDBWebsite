# Session/tests/test_views.py

import pytest
import datetime

from django.test import Client
from django.urls import reverse

from session.tests import factories

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

@pytest.mark.django_db
class TestSessionDetail:
    def test_session_detail_200(self):
        
        obj = factories.SessionFactory(
            date = datetime.date(2021, 10, 2)
        )
        client = Client()
        response = client.get(reverse('session_detail',
                              kwargs={'year': 2021, 'month': 10, 'day': 2}))
        
        assert response.status_code == 200, "Get 200 status for session.views.session_detail"
        