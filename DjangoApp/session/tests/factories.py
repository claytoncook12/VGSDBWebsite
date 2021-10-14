import factory
from pathlib import Path
import datetime

from django.conf import settings
from Session import models

class tune_typeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TuneType
    
    tune_type_id = 1
    tune_type_char = "reel"

class tuneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tune
    
    tune_id = 1
    name1 = "Tune Name #1"
    name2 = "Tune Name #2"
    name3 = "Tune Name #3"
    name4 = "Tune Name #4"
    TuneType = factory.SubFactory(tune_typeFactory)
    the_session_url = "https://www.youtube.com/embed/testthesessionurl"
    tune_info = "Some Test Tune Information"

class sessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Session
    
    session_id = 1
    name = "Session Name 1"
    date = datetime.date(2021, 1, 1)
    youtube_url = "https://www.youtube.com/embed/testyoutubesessionurl"

class name_yer_tuneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NameYerTune
    
    name_yer_tune_id = 1
    Tune = factory.SubFactory(tuneFactory)
    Session = factory.SubFactory(sessionFactory)
    youtube_teaching_url = "https://www.youtube.com/embed/testvalue"