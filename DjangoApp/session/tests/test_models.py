# session/tests/test_models.py

import pytest
from pathlib import Path

from django.conf import settings
from session.tests import factories

from django.core.exceptions import ValidationError

@pytest.mark.django_db
class Testname_yer_tune:
    def test_init(self):
        obj = factories.name_yer_tuneFactory()
        assert obj.pk == 1, "Should save an instance"
    
    def test_str(self):
        obj = factories.name_yer_tuneFactory()
        assert str(obj) == "01/01/2021 tune name #1", "Should have specific str"
    
    def test_clean1(self):
        with pytest.raises(ValidationError):
            obj = factories.name_yer_tuneFactory(
                youtube_teaching_url = "https://www.youtube.com/watch?v=NpQ8kEY9oq8"
            )
            obj.clean(), "Should raise error on clean due to file type not being .mp3"
    
    def test_clean2(self):
        obj = factories.name_yer_tuneFactory(
            youtube_teaching_url = "https://www.youtube.com/embed/I03EtvbmauY"
        )
        assert obj.pk ==1, "Should save an instance with embed youtube url"    