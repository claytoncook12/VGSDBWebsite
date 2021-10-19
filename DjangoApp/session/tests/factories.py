import factory
from pathlib import Path
import datetime

from django.conf import settings
from session import models

class TuneTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TuneType
    
    tune_type_char = "reel"

class KeyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Key
    
    key_type_char = "g"

class TuneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tune
    
    name1 = "Tune Name #1"
    name2 = "Tune Name #2"
    name3 = "Tune Name #3"
    name4 = "Tune Name #4"
    tune_type = factory.SubFactory(TuneTypeFactory)
    the_session_url = "https://www.youtube.com/embed/testthesessionurl"
    tune_info = "Some Test Tune Information"

class SessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Session
    
    name = "Session Name 1"
    date = datetime.date(2021, 1, 2)
    youtube_url = "https://www.youtube.com/embed/testyoutubesessionurl"

class PlayedTuneGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PlayedTuneGroup
    
    session = factory.SubFactory(SessionFactory)
    session_order_num = 1
    start_time = datetime.timedelta(seconds=100)
    end_time = datetime.timedelta(seconds=200)
    offertory = True

class PlayedTuneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PlayedTune
    
    tune = factory.SubFactory(TuneFactory)
    played_tune_group = factory.SubFactory(PlayedTuneGroupFactory)
    key = factory.SubFactory(KeyFactory)
    group_order_num = 1
    add_info = "some test info about the tune"


class NameYerTuneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NameYerTune
    
    tune = factory.SubFactory(TuneFactory)
    session = factory.SubFactory(SessionFactory)
    youtube_teaching_url = "https://www.youtube.com/embed/testvalue"

class TuneOfTheMonthFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TuneOfTheMonth

    tune = factory.SubFactory(TuneFactory)
    published_date = datetime.date(2021, 10, 16)
    youtube_teaching_url = "https://www.youtube.com/embed/testvalue"