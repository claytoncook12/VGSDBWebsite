# Session/tests/test_models.py

import pytest
from pathlib import Path

from django.conf import settings
from session.tests import factories

from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestTuneType:
    def test_init(self):
        obj = factories.TuneTypeFactory()
        assert obj.pk == 1, "Should save an instance"
    
    def test_str(self):
        obj = factories.TuneTypeFactory()
        assert str(obj) == 'reel', "str should be default tune_type"

@pytest.mark.django_db
class TestKey:
    def test_init(self):
        obj = factories.KeyFactory()
        assert obj.pk == 1, "Should save an instance"
    
    def test_str(self):
        obj = factories.KeyFactory()
        assert str(obj) == "g", "str should be default key_type_char"
    
    def test_save(self):
        obj = factories.KeyFactory(
            key_type_char = "G"
        )
        assert obj.key_type_char == "g", "key_type_char should be changed to lower case on save"

@pytest.mark.django_db
class TestTune:
    def test_init(self):
        obj = factories.TuneFactory()
        assert obj.pk == 1, "Should save an instance"
    
    def test_str(self):
        obj = factories.TuneFactory()
        assert str(obj) == "tune name #1 (reel)", "str should be default of factories"

@pytest.mark.django_db
class TestSession:
    def test_init(self):
        obj = factories.SessionFactory()
        assert obj.pk == 1, "Should save an instace"
    
    def test_str(self):
        obj = factories.SessionFactory()
        assert str(obj) == "01/02/2021: session name 1", "str should be default of factories"

@pytest.mark.django_db
class TestPlayedTuneGroup:
    def test_init(self):
        obj = factories.PlayedTuneGroupFactory()
        assert obj.pk == 1, "Should save an instance"
    
    def test_str(self):
        obj = factories.PlayedTuneGroupFactory()
        assert str(obj) == "01/02/2021: Song Group 1 [0:01:40 to 0:03:20]", "str should be default of factories"

@pytest.mark.django_db
class TestPlayedTune:
    def test_init(self):
        obj = factories.PlayedTuneFactory()
        assert obj.pk == 1, "Should save an instace"
    
    def test_str(self):
        obj = factories.PlayedTuneFactory()
        assert str(obj) == "01/02/2021 - Group 1 - 1 - tune name #1 (g) (reel)", "str should be default in factories"


@pytest.mark.django_db
class TestNameYerTune:
    def test_init(self):
        obj = factories.NameYerTuneFactory()
        assert obj.pk == 1, "Should save an instance"
    
    def test_str1(self):
        obj = factories.NameYerTuneFactory()
        assert str(obj) == "01/02/2021 tune name #1", "Should have specific str"
    
    def test_str2(self):
        obj = factories.NameYerTuneFactory(
            session = None
        )
        assert str(obj) == "tune name #1 (No Session Assigned)", "Should have specific str"
    
    def test_clean1(self):
        with pytest.raises(ValidationError):
            obj = factories.NameYerTuneFactory(
                youtube_teaching_url = "https://www.youtube.com/watch?v=NpQ8kEY9oq8"
            )
            obj.clean(), "Should raise error on clean due to file type not being .mp3"
    
    def test_clean2(self):
        obj = factories.NameYerTuneFactory(
            youtube_teaching_url = "https://www.youtube.com/embed/I03EtvbmauY"
        )
        assert obj.pk ==1, "Should save an instance with embed youtube url"

@pytest.mark.django_db
class TestTuneOfTheMonth:
    def test_init(self):
        obj = factories.TuneOfTheMonthFactory()
        assert obj.pk == 1, "Should save an instance"
    
    def test_str(self):
        obj = factories.TuneOfTheMonthFactory()
        assert str(obj) == "10/16/2021 tune name #1", "str should match default"