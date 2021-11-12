# Session/tests/test_views.py
from django.contrib.auth.models import User

import pytest
import datetime

from django.test import Client
from django.urls import reverse

from session.tests import factories

PASSWORD = "password"

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
    def test_session_detail(self):        
        obj1 = factories.SessionFactory(
            date=datetime.date(2021, 10, 2)
        )
        obj2 = factories.PlayedTuneGroupFactory(
            session=obj1
        )
        obj3 = factories.PlayedTuneFactory(
            played_tune_group=obj2
        )
        
        client = Client()
        response = client.get(reverse('session_detail',
                              kwargs={'year': 2021, 'month': 10, 'day': 2}))
        
        assert response.status_code == 200, "Get 200 status for session.views.session_detail"

        assert obj1.name.title() in response.content.decode(), "The session.session_detail view shows Session.name"

        # Test Display of PlayedTuneGroup Start and End Times
        assert str(obj2.start_time) in response.content.decode(), "The session.session_detail view shows PlayedTuneGroup.start_time"
        assert str(obj2.end_time) in response.content.decode(), "The session.session_detail view shows PlayedTuneGroup.end_time"

        # Test Display of PlayedTune
        assert obj3.tune.name1.title() in response.content.decode(), "The session.session_Detail view shows PlayedTune information"


@pytest.mark.django_db
class TestTunesAll:
    @pytest.mark.skip(reason="""Uses session.views.Concat(Aggregate) to display keys that have been
                                played for that tune which is a PostgreSQL sepcific aggregate
                                function and during testing I'm using a sqlite3 in-memory database
                            """)
    def test_tune_all(self):
        obj1 = factories.TuneFactory()

        obj2 = factories.PlayedTuneFactory(
            tune=obj1
        )

        client = Client()
        response = client.get(reverse('tunes_all'))

        assert response.status_code == 200, "Get 200 status for session.views.tune_all"

        # Show Table Information of Tune
        assert obj2.tune.name1 in response.content.decode(), "The session.tunes_all view shows Tune.name1"
        assert obj2.tune.tune_type in response.content.decode(), "The session.tunes_all view shows Tune.tune_type"
        assert obj2.key in response.content.decode(), "The session.tunes_all view shows Tune.name1"


@pytest.mark.django_db
class TestTuneDetail:
    def test_tune_detail(self):
        PLAYED_TIMES_STR = "Played: 1"

        # Setup Tune and Played Once
        obj1 = factories.SessionFactory(
            date=datetime.date(2021, 10, 2)
        )
        obj2 = factories.PlayedTuneGroupFactory(
            session=obj1
        )
        obj3 = factories.PlayedTuneFactory(
            played_tune_group=obj2
        )

        client = Client()
        response = client.get(
            reverse('tune_detail',
            kwargs={'tune_id': obj3.tune.tune_id})
        )
        
        assert response.status_code == 200, "Get 200 status for session.views.tune_detail"

        # Test Display of Proper Tune data
        assert obj3.tune.name1.title() in response.content.decode(), "Test That Tune.name1 is display"
        assert str("Tune Type: " + obj3.tune.tune_type.tune_type_char.title()) \
            in response.content.decode(), "Test That Tune.tune_type is display"
        assert PLAYED_TIMES_STR in response.content.decode(), "Test that Tune shows as played once"


@pytest.mark.django_db
class TestNameyertuneAll:
    def test_nameyertune_all(self):
        obj = factories.NameYerTuneFactory()

        client = Client()
        response = client.get(reverse('nameyertune_all'))

        assert response.status_code == 200, "Get 200 status for session.views.nameyertune_all"

        # Test Deiplay of Proper NameYerTune data
        assert obj.tune.name1.title() in response.content.decode(), "Test that Tune.name1 shows"


@pytest.mark.django_db
class TestYoutubeLoopTest2:
    def test_youtube_loop_test1(self):

        client = Client()
        response = client.get(reverse('youtube_loop_test2'))

        assert response.status_code == 200, "Get 200 status for session.views.youtube_loop_test2"
    
@pytest.mark.django_db
class TestAdminLinksTab:
    def test_admin_links_view_normal_user(Self):
        client = Client()
        response = client.get(reverse('admin_links'))

        assert response.status_code == 302, "302 status for session.views.adminlinks when user is not superuser in"
    
    def test_admin_links_view_superuser_user(Self):
        # Create SuperUser for testing
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', PASSWORD)
        
        client = Client()
        # You'll need to log him in before you can send requests through the client
        client.login(username=my_admin.username, password=PASSWORD)
        
        response = client.get(reverse('admin_links'))
        assert response.status_code == 200, "200 status for session.views.adminlinks when user is superuser"

@pytest.mark.django_db
class TestSessionJSON:
    def test_session_json_normal_user(self):
        client = Client()
        response = client.get(reverse('session_json'))

        assert response.status_code == 302, "302 status for session.views.session_json when user is not superuser in"
    
    def test_asession_json_view_superuser_user(Self):
        # Create SuperUser for testing
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', PASSWORD)
        
        client = Client()
        # You'll need to log him in before you can send requests through the client
        client.login(username=my_admin.username, password=PASSWORD)
        
        response = client.get(reverse('session_json'))
        assert response.status_code == 200, "200 status for session.views.session_json when user is superuser"